
```
1. contraposition on strict rules
2. search for the rules with conclusions only and generate their respective arguments (verify if the rule has a conclusion?)
2.1 add the arguments in the bf
3. in a different function have a list of all the rules minus the rules for the intial arguments
3.1 for each rule in the list of rules, generate the arguments
3.2 add the respective arguments in the bf
4. during this step we will try to generate the remaining arguments
4.1 go through all the rules once and again and for each rule iterate over the bf and check if you can genereate a new argument for it and add it to the bf
4.2. iterate over the whole bf once again and check if you can generate a new argument and then move to the next rule
4.3 repeate 4.1 and 4.2 until no new arguments are generated

```