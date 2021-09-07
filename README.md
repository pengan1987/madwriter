# Mad Writer

Release as [NFT on OpenSea](https://opensea.io/assets/0x495f947276749ce646f68ac8c248420045cb7b5e/85082193235839641358202176184789853165871417855160442130207862834404947656705)

This work is a Chinese generative literature script which compose articles with remixing articles from my writing project. The original article will be downloaded from IPFS or Matataki.io as data source and parsed to vocabulary lists then randomly combined with some rules to making new article.

Also, this work is a telematic/terminal art originally designed for dumb terminals with Chinese (GBK) capability, I tested it with several Newland NL-3400L networked Chinese terminals. A DOS communication software e.g. Telix with Chinese DOS environment also works. However, you might got some garbled text because most Chinese DOS environment only supports GB2312 and missing some characters in GBK.

- mad.py: Original version, fetch data from Matataki and output text
- maddownload.py, madlocal.py: Offline exhibition version, running with pre-download articles
- madoffline.py: Another offline version, running with prepared text files

Live demo: [CompuMuseum](http://www.compumuseum.com/emularity.html?emularity=dosbox-websocket&machineurl=emularity-machine/madwriter.json)