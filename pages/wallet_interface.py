from bitcoinlib.wallets import Wallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic


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
        try:
            self.wallet = Wallet.import_mnemonic(
                "btc_wallet",
                self.mnemonic,
                network='bitcoin',
                witness_type='segwit',
            )
        except:
            wallet_delete("btc_wallet")
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
