<!---------------------------------------------------------------------------------
Copyright: (c) BLS OPS LLC.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------->

## [-] REFERENCES

1. https://docs.splunk.com/Documentation/SplunkCloud/latest/SearchReference/Join


## [-] NOTES

- TBD


## [-] USE CASES

__============ WEB PAGE VISITS ============__

__PROBLEM STATEMENT__  - Which user, identified by their email address, edited their profile before placing an order over $1000 in the same clickstream? Answer guidance: Provide the user ID, not other values found from the profile edit, such as name."form_key" remains constant during the clikcstream.

__============ raw ============__

        dest_content: {"payment_methods":[{"code":"braintree_cc_vault","title":"Stored Cards (Braintree)"},{"code":"braintree_paypal","title":"PayPal (Braintree)"},{"code":"braintree","title":"Credit Card (Braintree)"},{"code":"checkmo","title":"Check \/ Money order"}],"totals":{"grand_total":120,"base_grand_total":120,"subtotal":100,"base_subtotal":100,"discount_amount":0,"base_discount_amount":0,"subtotal_with_discount":100,"base_subtotal_with_discount":100,"shipping_amount":20,"base_shipping_amount":20,"shipping_discount_amount":0,"base_shipping_discount_amount":0,"tax_amount":0,"base_tax_amount":0,"weee_tax_applied_amount":null,"shipping_tax_amount":0,"base_shipping_tax_amount":0,"subtotal_incl_tax":100,"shipping_incl_tax":20,"base_shipping_incl_tax":20,"base_currency_code":"USD","quote_currency_code":"USD","items_qty":4,"items":[{"item_id":302,"price":25,"base_price":25,"qty":4,"row_total":100,"base_row_total":100,"row_total_with_discount":0,"tax_amount":0,"base_tax_amount":0,"tax_percent":0,"discount_amount":0,"base_discount_amount":0,"discount_percent":0,"price_incl_tax":25,"base_price_incl_tax":25,"row_total_incl_tax":100,"base_row_total_incl_tax":100,"options":"[]","weee_tax_applied_amount":null,"weee_tax_applied":null,"name":"Mens Frothly Tee"}],"total_segments":[{"code":"subtotal","title":"Subtotal","value":100},{"code":"shipping","title":"Shipping & Handling (Flat Rate - Fixed)","value":20},{"code":"tax","title":"Tax","value":0,"extension_attributes":{"tax_grandtotal_details":[]}},{"code":"grand_total","title":"Grand Total","value":120,"area":"footer"}]}}

        Cookie: store=default; mage-translation-storage=%7B%7D; mage-translation-file-version=%7B%7D; form_key=P5QjF09iujN41DsK; PHPSESSID=io259vpm8q9hbsjcjalum14ms3; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; mage-cache-sessid=true; mage-messages=; private_content_version=3ff42898bcbcd465fedd690b41db0810; X-Magento-Vary=9bf9a599123e6402b85cde67144717a08b817412; section_data_ids=%7B%22cart%22%3A1502993675%2C%22customer%22%3A1502993675%2C%22compare-products%22%3A1502993675%2C%22product_data_storage%22%3A1502993675%2C%22last-ordered-items%22%3A1502993675%2C%22directory-data%22%3A1502993675%2C%22review%22%3A1502993675%2C%22wishlist%22%3A1502993675%2C%22recently_viewed_product%22%3A1502993675%2C%22recently_compared_product%22%3A1502993675%2C%22paypal-billing-agreement%22%3A1502993675%2C%22messages%22%3A1502993675%7D

        src_content: {"addressInformation":{"shipping_address":{"countryId":"US","regionId":"62","regionCode":"WA","region":"Washington","street":["1654 Virginia Ave"],"company":"","telephone":"206-548-9033","postcode":"98101","city":"Seattle","firstname":"Sanaa","lastname":"Arellano","save_in_address_book":1},"billing_address":{"countryId":"US","regionId":"62","regionCode":"WA","region":"Washington","street":["1654 Virginia Ave"],"company":"","telephone":"206-548-9033","postcode":"98101","city":"Seattle","firstname":"Sanaa","lastname":"Arellano","save_in_address_book":1,"saveInAddressBook":null},"shipping_method_code":"flatrate","shipping_carrier_code":"flatrate"}}

__============ raw ============__

__APPROACH__ 

        * sourcetype=stream:http site=*froth* *address* *shipping* NOT uri="*\.js"
        | rex field=cookie "form_key=(?<key>[0-9A-Za-z]{1,}?)\;"
        | spath input=src_content 
        | rename "addressInformation.shipping_address.firstname" AS first
        | rename "addressInformation.shipping_address.lastname" AS last
        | spath input=dest_content 
        | rename "totals.grand_total" AS total
        | WHERE total > 999
        | join key max=0 [search * sourcetype=stream:http site=*froth* uri=*account\/edit*
            | rex field=cookie "form_key=(?<key2>[0-9A-Za-z]{1,}?)\;"
            | table key2 uri
            | rename key2 as key]
        | table first last total key uri

__STEPS EXPLAINED__

1. Retrieve events with home and billing shipping addresses for all froth.ly websites
2. rex - extract the key from the cookie. This allows us to associate a request with a specific user
3. spath - assign the src_content to input. This allows us to leverage and search XML much more easily
4. rename - rename 2 fields from the source content data
5. spath - assign the dest_content to input. This allows us to leverage and search XML much more easily
6. rename - rename a field in the dest_content
7. where - filter out events where the total amount spent is > $999
8. join - join on “key”. This will look for events where the user edited their account information, extract the key from the cookie, create a table and rename the key field.
9. table - now we join and review the results. These are key values for users who spent > $999 and edited their account information

__============ DUMPING LSASS ============__

__PROBLEM STATEMENT__ - Find a malicious process that touched the lsass process. In this case the SharpHound tool had been used to dump lsass.exe

__APPROACH__ 

        index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 host=windows1
        | fields ProcessGUID Message ParentImage Image ParentCommandLine
        | rename ProcessGUID as ParentProcessGUID
        | rex field=Message "Company: (?<Company>.+)"
        | join ParentProcessGUID [search index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=10 | fields ParentProcessGUID TargetImage GrantedAccess]
        | search TargetImage="C:\\Windows\\System32\\lsass.exe" NOT Company="Microsoft Corporation"
        | table ParentImage Image TargetImage GrantedAccess ParentCommandLine

__STEPS EXPLAINED__

1. Retrieve process creation events from the target host
2. fields - Select fields to bring forward in the search pipeline
3. rename - This is important since we need to take the GUID for each process created and assume it MIGHT be the parent process that targets lsass.exe
4. rex - extract the company name that “signed” the executable/image associated with the process
5. join - execute a join on the ParentProcessGUID. The second seach is going to find any event where ANY process was “touched” and bring forward specific fields
6. search - find lsass specific events only unrelated to Microsoft
7. table - show results. Now identify those process that SHOULD NOT interact with lsass. 


## [-] TAGS

\#join #rex #spath #rename #where #fields #search #table
