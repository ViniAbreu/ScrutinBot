# ScrutinBot

* **Scanners**
  * [SQL Injection](https://github.com/SrBiggs/ScrutinBot/blob/master/doc/translations/README-pt-br.md#scanner-sql-injection)
  * [XSS](https://github.com/SrBiggs/ScrutinBot/blob/master/doc/translations/README-pt-br.md#scanner-xsscross-site-scripting)
  * [LFI](https://github.com/SrBiggs/ScrutinBot/blob/master/doc/translations/README-pt-br.md#scanner-lfilocal-file-include)
* **Crawlers**
  * [Bing](https://github.com/SrBiggs/ScrutinBot/blob/master/doc/translations/README-pt-br.md#crawler-bing)
* **Criptografia**
  * [Encriptar](https://github.com/SrBiggs/ScrutinBot/blob/master/doc/translations/README-pt-br.md#criptografia)
  * [Decriptar](https://github.com/SrBiggs/ScrutinBot/blob/master/doc/translations/README-pt-br.md#descriptografar)
* **Geradores**
  * [Dork](https://github.com/SrBiggs/ScrutinBot/blob/master/doc/translations/README-pt-br.md#geradores)
  
# Scanners

## Scanner SQL Injection
----
>**Comando:** `/sql`

>**Syntax:** `/sql [url]`

>**Argumento Esperado:** `url`

>Este comando iniciará um scanner procurando por falhas de injeção SQL.

>![command_/sql](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_sql.png)


## Scanner XSS(Cross-Site-Scripting)
----
>**Comando:** `/xss`

>**Syntax:** `/xss [url]`

>**Argumento Esperado:** `url`

>**Payloads para o comando:** [Payloads_XSS]()

>Este comando iniciará um scanner procurando por falhas XSS.

>![command_/xss](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_xss.png)

## Scanner LFI(Local File Include)
----
>**Comando:** `/lfi`

>**Syntax:** `/lfi [url]`

>**Argumento Esperado:** `url`

>**Payloads para o comando:** [Payloads_LFI]()

>Este comando iniciará um scanner procurando por falhas XSS.

>![command_/lfi](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_lfi.png)


# Crawlers

## Crawler Bing
----
>**Comando:** `/bing`

>**Argumento Esperado:** `dork`

>Este comando irá crawlear links no motor de busca Bing

>![command_/bing](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_bing.png)

# Criptografia

## Encriptar
>**Comando:** `/encrypt`

>**Syntax:** `/encrypt [algoritmo] [texto]`

>**Argumento Esperado:** `algoritmo de criptografia`

>**Algoritmos Suportados:** `url,b64,hex`

>Este comando irá criptografar textos normais nos algoritmos suportados

>![command_/encrypt_url](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_encrypt_url.png)

>![command_/encrypt_b64](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_encrypt_b64.png)

>![command_/encrypt_hex](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_encrypt_hex.png)

## Descriptografar
>**Comando:** `/decrypt`

>**Syntax:** `/decrypt [algoritmo] [cifra]`

>**Argumento Esperado:** `algoritmo de criptografia`

>**Algoritmos Suportados:** `url,b64,hex`

>Este comando irá descriptografar textos cifrados nos algoritmos suportados

>![command_/decrypt_url](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_decrypt_url.png)

>![command_/decrypt_b64](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_decrypt_b64.png)

>![command_/decrypt_hex](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_decrypt_hex.png)

# Geradores

## Dork
----
>**Comando:** `/dork`

>**Syntax:** `/dork [nameFile] [Paramter]`

>**Argumentos Esperados:** `[nameFile] [Paramter]`

>Este comando irá gerar dorks baseado em um simples algoritmo

>![command_/dork](https://github.com/SrBiggs/ScrutinBot/blob/master/screenshots/command_generator_dork.png)
