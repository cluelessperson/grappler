import grappler

b = grappler.BitcoinCoreConnector(
    host="bitcoin.cluelessperson.com",
    port=8333,
    ssl=True,
    timeout=5,
    network="mainnet"
)

e = grappler.ElectrumXConnector(
    host="bitcoin.cluelessperson.com",
    port=50002,
    ssl=True,
    timeout=5
)
e.send("server.version")
e.send("blockchain.address.get_balance","1CFF6NW7oSQAkbbH9EikVVyq3gcH5yEpJM")
