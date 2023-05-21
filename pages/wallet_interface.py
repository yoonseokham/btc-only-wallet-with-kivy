from bitcoinlib.wallets import Wallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic
from embit import script, bip32, bip39, psbt
from embit.networks import NETWORKS
from binascii import unhexlify, hexlify, a2b_base64, b2a_base64


class WalletInterface:
    def __init__(
        self,
        length=12,
        mnemonic=None,
    ):
        if mnemonic:
            self.mnemonic = mnemonic
        else:
            self.mnemonic = self.generate_mnemonic(length)
        # these are test mnemonic no coins haha
        self.mnemonic = "alien visual jealous source coral memory embark certain radar capable clip edit"
        try:
            wallet_delete("btc_wallet")
            self.wallet = Wallet.import_mnemonic(
                "btc_wallet",
                self.mnemonic,
                network='bitcoin',
                witness_type='segwit',
            )
        except:
            # wallet_delete("btc_wallet")
            self.wallet = Wallet.create(
                "btc_wallet",
                keys=self.mnemonic,
                network='bitcoin',
                witness_type='segwit',
            )
        # todo(yoonseok)
        # store btc private key in local storage

    @staticmethod
    def generate_mnemonic(length=12):
        return {
            12: Mnemonic().generate(strength=128),
            24: Mnemonic().generate(strength=256)
        }[length]

    def get_address(self):
        return self.wallet.get_key().address

    def get_xpub(self):
        return self.wallet.public_master().wif

    def sign_psbt(self, b64_psbt):
        seed = bip39.mnemonic_to_seed(self.mnemonic)
        root = bip32.HDKey.from_seed(seed, version=NETWORKS["test"]["xprv"])
        fingerprint = root.child(0).fingerprint
        # first convert it to binary
        raw = a2b_base64(b64_psbt)
        # then parse
        tx = psbt.PSBT.parse(raw)
        total_in = 0
        for inp in tx.inputs:
            total_in += inp.witness_utxo.value
        change_out = 0  # value that goes back to us
        send_outputs = []
        for i, out in enumerate(tx.outputs):
            # check if it is a change or not:
            change = False
            # should be one or zero for single-key addresses
            for pub in out.bip32_derivations:
                # check if it is our key
                if out.bip32_derivations[pub].fingerprint == fingerprint:
                    hdkey = root.derive(out.bip32_derivations[pub].derivation)
                    mypub = hdkey.key.get_public_key()
                    if mypub != pub:
                        raise ValueError("Derivation path doesn't look right")
                    # now check if provided scriptpubkey matches
                    sc = script.p2wpkh(mypub)
                    if sc == tx.tx.vout[i].script_pubkey:
                        change = True
                        continue
            if change:
                change_out += tx.tx.vout[i].value
            else:
                send_outputs.append(tx.tx.vout[i])
        fee = total_in - change_out
        for out in send_outputs:
            fee -= out.value

        # sign the transaction
        tx.sign_with(root)
        raw = tx.serialize()
        # convert to base64
        b64_psbt = b2a_base64(raw)
        # somehow b2a ends with \n...
        if b64_psbt[-1:] == b"\n":
            b64_psbt = b64_psbt[:-1]
        return b64_psbt.decode('utf-8')