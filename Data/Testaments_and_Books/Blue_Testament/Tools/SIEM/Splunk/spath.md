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

1. https://docs.splunk.com/Documentation/SplunkCloud/8.1.2101/SearchReference/Spath


## [-] NOTES

- The spath command enables you to extract information from the structured data formats XML and JSON. The command stores this information in one or more fields. The command also highlights the syntax in the displayed events list.


## [-] USE CASES

__============ MULTIPLE CUSTOMERS SAME ADDRESS ============__

__PROBLEM STATEMENT__ - Find shipping and billing addresses that may be getting used by the same customer. 

__APPROACH__ 

__============ raw ============__

        src_content: {"addressInformation":{"shipping_address":{"countryId":"US","regionId":"62","regionCode":"WA","region":"Washington","street":["1654 Virginia Ave"],"company":"","telephone":"206-548-9033","postcode":"98101","city":"Seattle","firstname":"Sanaa","lastname":"Arellano","save_in_address_book":1},"billing_address":{"countryId":"US","regionId":"62","regionCode":"WA","region":"Washington","street":["1654 Virginia Ave"],"company":"","telephone":"206-548-9033","postcode":"98101","city":"Seattle","firstname":"Sanaa","lastname":"Arellano","save_in_address_book":1,"saveInAddressBook":null},"shipping_method_code":"flatrate","shipping_carrier_code":"flatrate"}}

__============ raw ============__

        * sourcetype=stream:http site=*froth* *address* *shipping* NOT uri="*\.js"
        | spath input=src_content 
        | rename "addressInformation.shipping_address.firstname" AS first
        | rename "addressInformation.shipping_address.lastname" AS last
        | rename "addressInformation.shipping_address.telephone" AS telephone
        | rename "addressInformation.shipping_address.street{}" AS shipping
        | rename "addressInformation.billing_address.street{}" AS billing
        | WHERE len(shipping) > 0 AND len(billing) > 0
        | stats dc(last) BY shipping billing
        | sort - dc(last)

__STEPS EXPLAINED__

1. Retrieve events with home and billing shipping addresses for all froth.ly websites
2. spath - assign the src_content to input. This allows us to leverage and search XML much more easily
4. rename - rename 4 fields from the source content data and based on the SPATH schema
5. where - filter out events where the shipping and billing addresses are NOT NULL
6. stats - do a distinct count dc() on last name by shipping and billing address
7. Wherever you have high cunts you'll have mutliple customers using those same address pairs


## [-] TAGS

\#spath #rename #where #stats #sort
