import undetected_chromedriver as uc

driver = uc.Chrome(headless=True, use_subprocess=False)
driver.get("https://www.avito.ru/web/1/js/items?locationId=637640&categoryId=31")
# driver.save_screenshot("nowsecure.png")
