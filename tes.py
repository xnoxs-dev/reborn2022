from reborn2022.recaptcha import solver_recaptcha

token = solver_recaptcha(url, site_key, headless)
print(token)
