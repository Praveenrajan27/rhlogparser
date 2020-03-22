# rhlogparser
This repo is for parsing a simple log and display on Flask API built with Swagger

The APP recieves a CI log file of the form below and parses into specific components into JSON format

```
GOCACHE=off go test -timeout 20m -v${WHAT:+ -run="$WHAT"} ./test/e2e/
[ 0]ENTER: /usr/local/src/pkg/apis/machineconfiguration.openshift.io/v1/register.go:28 0
[ 0]EXIT:   /usr/local/src/src/github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go:28 0
[ 0]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/pkg/generated/clientset/versioned/scheme/register.go:19 0
[ 0]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go:32         addKnownTypes
[ 0]EXIT:   /usr/local/src/github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go:32         addKnownTypes
[ 0]EXIT:   /usr/local/src/golang/src/github.com/openshift/machine-config-operator/pkg/generated/clientset/versioned/scheme/register.go:19 0
=== RUN   TestMCDToken
 10 [ 1]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/test/e2e/mcd_test.go:21 TestMCDToken
 11 [ 0]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/cmd/common/client_builder.go:34 NewClientBuilder
 12 [ 0]EXIT:   /usr/local/src/github.com/openshift/machine-config-operator/cmd/common/client_builder.go:34 NewClientBuilder
 13 [ 0]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/cmd/common/client_builder.go:22 KubeClientOrDie
 14 [ 0]EXIT:   /usr/local/src/github.com/openshift/machine-config-operator/cmd/common/client_builder.go:22 KubeClientOrDie
 15 [ 1]EXIT:   /usr/local/src/github.com/openshift/machine-config-operator/test/e2e/mcd_test.go:21 TestMCDToken
 16 --- PASS: TestMCDToken (3.86s)
```



```
{
  "result": [{
    "operation": "ENTRY",
    "filename": "/usr/local/src/github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go",
    "line_number": 32,
    "name": "addKnownTypes"
  },
  {
    "operation": "EXIT",
    "filename": "/usr/local/src/src/github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go",
    "line_number": 28,
    "name": "anonymous"
  }]
}
```

The "name" is "anonymous" wherever it encounters an invalid function name(like '0' in the above logs). A valid function name follows the following rule: must begin with (unicode_letter or _), and can end with many (unicode_letter, unicode_digit or _).



## Design Specfication

The underlying logic of parsing the log lines are built using regex patterns and slicing using python. The logic is available in the package called CILogParser which is available in the venv directory
A flask Application is built on top of this that recieves the log file (either .log or .txt) as input. The API was designed using the OpenAPI 2.0 specification built using swagger UI editor. The App has a single POST method that accepts the file as input and responds back with the output in the desired specofied format as above. The variation of Flask called the connexion package was used to interact between the Swagger Spec and the flask Application.

```
├─── app.py
├─── config.py
├─── controller.py
├─── requirements.txt
│   
├───spec
│   ├───swagger.yaml
│       
│       
├───venv
   │   
   ├───CILogParser
      ├─── CILogParser.py
      ├─── __init__.py
```

The App initialization and the spec invokation are done at the app.py file. 
The Config file has 3 levels of specifications

1. App level configs like Allowable file size as input and JSON serilazable sort option are defined
2. File upload configs like File directory, and extensions allowed are specifies
3. option to exclude the testcases log entries are also mentioned here. Since it was unclear if the build entries only or even the testcases entries were to be parsed. THis flag can be used to switch both ways

It also has developer and tester specfication that inherits from the base Config class

The controller file has the logic of reading the file from the API and validating the file extension. The file is first saved into disk to handle high volume input files. they are then fetched and then makes a call to the package CIlogParser and return the JSON object

The Spec folder has the SWAG specfification based on OPenAPI 2.0 for the API options. Here there is a need for only one POST method for which the specs are defined

CILogParser is the class that have the underlying logic to parse in the specified format. The Parser uses the config and different regex patterns to parse as instructed. The dictionary is formed based on these extracted values and sent as a generator. The controller file then JSONifies this and sends it to the calling API


#### Assumptions:
- The code expects a single line to have all the information for a JSON entry
- The parsed example provided is only a sample. All the lines containing ENTER and EXIT needs to be parsed

