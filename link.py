from shopee_affiliate import ShopeeAffiliate
appid = "11329420170" # Your appid
secret = "7IR5CEE2UZXUIEB7SLFR5E6CDYVSV5XT" # Your secret
sa = ShopeeAffiliate(appid, secret)
res = sa.generateShortLink("https://www.shopee.co.id/mall")
print("shortlink:", res)