const rdf = '@prefix dct: <http://purl.org/dc/terms/> .\n\
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\
@prefix dcso: <https://w3id.org/dcso/ns/core#> .\n\
@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n\
@prefix dcs-lang: <https://w3id.org/dcso/id/iso639-3/> .\n\
\n\
# DMP\n\
<https://demo.ds-wizard.org/questionnaires/00f2e7b7-a1c8-42a1-a2fc-2f93dbdbaa76>\n\
  a dcso:DMP ;\n\
  dct:title "maDMP" ;\n\
  dct:description "This maDMP has been created using Data Stewardship Wizard (DSW, ds-wizard.org) and is based on knowledge model Common DSW Knowledge Model (dsw:root:2.3.0). The questionnaire used for this DMP is identified by UUID \\\"00f2e7b7-a1c8-42a1-a2fc-2f93dbdbaa76\\\" within https://demo.ds-wizard.org DSW instance." ;\n\
  dct:language dcs-lang:eng ;\n\
  dcso:ethicalIssuesExist "unknown" ;\n\
  dcso:ethicalIssuesDescription "Non-reference dataset (unknown name) does not need an extension of consent because it does not contain personal data." ;\n\
  dcso:hasDMPId <https://demo.ds-wizard.org/questionnaires/00f2e7b7-a1c8-42a1-a2fc-2f93dbdbaa76/identifier> ;\n\
  dcso:hasContact <https://orcid.org/abcd> ;\n\
  dcso:hasContributor\n\
    [ a dcso:Contributor ;\n\
      dcso:hasContributorId\n\
        [ a dcso:ContributorId ;\n\
          dcso:identifier_type "orcid" ;\n\
          dct:identifier "abcd" ;\n\
        ] ;\n\
      foaf:mbox "karel.barel@example.com" ;\n\
      dcso:role "contact person" ;\n\
      foaf:name "Karel Barel" ;\n\
    ] ,\n\
    [ a dcso:Contributor ;\n\
      dcso:hasContributorId\n\
        [ a dcso:ContributorId ;\n\
          dcso:identifier_type "orcid" ;\n\
          dct:identifier "456743212345" ;\n\
        ] ;\n\
      foaf:mbox "martin.vomacka@example.com" ;\n\
      dcso:role "data steward" ;\n\
      foaf:name "Martin Vom\u00e1\u010dka" ;\n\
    ] ,\n\
    [ a dcso:Contributor ;\n\
      dcso:hasContributorId\n\
        [ a dcso:ContributorId ;\n\
          dcso:identifier_type "orcid" ;\n\
          dct:identifier "SADFGH" ;\n\
        ] ;\n\
      foaf:mbox "v.slechtova@example.com" ;\n\
      dcso:role "other" ;\n\
      foaf:name "Vojt\u011b\u0161ka \u0160lechtov\u00e1" ;\n\
    ] ;\n\
  dct:created "2022-02-23T08:55:35Z"^^xsd:dateTime ;\n\
  dct:modified "2022-02-23T08:55:35Z"^^xsd:dateTime .\n\
\n\
# DMP identifier\n\
<https://demo.ds-wizard.org/questionnaires/00f2e7b7-a1c8-42a1-a2fc-2f93dbdbaa76/identifier> a dcso:DMPId ;\n\
  dcso:identifier_type "url" ;\n\
  dct:identifier "https://demo.ds-wizard.org/questionnaires/00f2e7b7-a1c8-42a1-a2fc-2f93dbdbaa76" .\n\
\n\
# DMP contact\n\
<https://orcid.org/abcd> a dcso:Contact ;\n\
  dcso:hasContactId <https://orcid.org/abcd/identifier> ;\n\
  foaf:mbox "karel.barel@example.com" ;\n\
  foaf:name "Karel Barel" .\n\
\n\
<https://orcid.org/abcd/identifier> a dcso:ContactId ;\n\
  dcso:identifier_type "orcid" ;\n\
  dct:identifier "abcd" .\n\
\n\
\n\
# This file has been exported from Data Stewardship Wizard (ds-wizard.org)\n\
# It is using DCSO 3.0.2 (see https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard)'

export default rdf