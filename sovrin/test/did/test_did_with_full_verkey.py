"""
Full verkey tests
    Add a nym (16 byte, base58) with a full verkey (32 byte, base58) (Form 1)
        { type: NYM, dest: <id2>, verkey: <32byte key> }
    Retrieve the verkey.
        { type: GET_NYM, dest: <id2> }
    Verify a signature from this identifier
    Change a verkey for a nym with a full verkey.
        { type: NYM, dest: <id2>, verkey: <32byte ED25519 key> }
    Retrieve new verkey
        { type: GET_NYM, dest: <id2> }
    Verify a signature from this identifier with the new verkey
"""
from plenum.test.eventually import eventually

from sovrin.common.identity import Identity
from sovrin.test.did.conftest import pf
from sovrin.test.did.helper import chkVerifyForRetrievedIdentity, \
    updateWalletIdrWithFullKeySigner, updateSovrinIdrWithFullKey, \
    fetchFullVerkeyFromSovrin, checkFullVerkeySize
from sovrin.test.helper import createNym


@pf
def didAddedWithFullVerkey(addedSponsor, looper, sponsor, sponsorWallet,
                          wallet, fullKeyIdr):
    """{ type: NYM, dest: <id1> }"""
    createNym(looper, fullKeyIdr, sponsor, sponsorWallet,
              verkey=wallet.getVerkey(fullKeyIdr))
    return wallet


@pf
def newFullKey(wallet, fullKeyIdr):
    return updateWalletIdrWithFullKeySigner(wallet, fullKeyIdr)


@pf
def didUpdatedWithFullVerkey(didAddedWithFullVerkey, looper, sponsor,
                            sponsorWallet, fullKeyIdr, newFullKey, wallet):
    """{ type: NYM, dest: <id1>, verkey: <vk1> }"""
    updateSovrinIdrWithFullKey(looper, sponsorWallet, sponsor, wallet,
                               fullKeyIdr, newFullKey)


@pf
def newVerkeyFetched(didAddedWithFullVerkey, looper, sponsor, sponsorWallet,
                     fullKeyIdr, wallet):
    """{ type: GET_NYM, dest: <id1> }"""
    fetchFullVerkeyFromSovrin(looper, sponsorWallet, sponsor, wallet,
                              fullKeyIdr)


def testAddDidWithVerkey(didAddedWithFullVerkey):
    pass


def testRetrieveFullVerkey(didAddedWithFullVerkey, looper, sponsor,
                            sponsorWallet, wallet, fullKeyIdr):
    """{ type: GET_NYM, dest: <id1> }"""
    identity = Identity(identifier=fullKeyIdr)
    req = sponsorWallet.requestIdentity(identity,
                                        sender=sponsorWallet.defaultId)
    sponsor.submitReqs(req)

    def chk():
        retrievedVerkey = sponsorWallet.getIdentity(fullKeyIdr).verkey
        assert retrievedVerkey == wallet.getVerkey(fullKeyIdr)
        checkFullVerkeySize(retrievedVerkey)

    looper.run(eventually(chk, retryWait=1, timeout=5))
    chkVerifyForRetrievedIdentity(wallet, sponsorWallet, fullKeyIdr)


def testChangeVerkeyToNewVerkey(didUpdatedWithFullVerkey):
    pass


def testRetrieveChangedVerkey(didUpdatedWithFullVerkey, newVerkeyFetched):
    pass


def testVerifySigWithChangedVerkey(didUpdatedWithFullVerkey, newVerkeyFetched,
                                   sponsorWallet, fullKeyIdr, wallet):
    chkVerifyForRetrievedIdentity(wallet, sponsorWallet, fullKeyIdr)
