# courtlistener

1. Create a file called `token.txt` with only the courtlistener API token as the content\
https://www.courtlistener.com/help/api/rest/

2. Update the urls for the dockets in `docket_urls.txt`

3. To add fields
- Add fields to `docket_fields_to_include.txt` or leave it blank to get all the fields

Currently, jsons will be created upon run for each docket inside `/model/jsons/`

## Work in prog!
### Docket db for now
|Field|Type|Description|
|-|-|-|
|id|int|docket id|
|case_name|string|case name|
|date-filed|date|date the case was filed|
|appealed|boolean|if the case is coming from an appeal|c


---
## My basic outline - a sad un-wireframe if you will
**Case**: name\
**Judge**: namey name\
**Filed**: date\
**Updated**: date\
**Changes made today**: 
- [X entry created]
- [Document updated]

[**View all Entries**](google.com)
