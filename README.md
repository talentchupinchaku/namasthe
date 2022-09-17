# namasthe

* Add your Azure Function in another folder, just like first_andi
* Add your dependencies to requirements.txt
* Please try not to maintain state in your function as it does a fresh start on every run. 
* If you **must** store state, please DM me and we can see if we can use Blob Storage 
* Test your function in your local, in my case, the code is in first.py [here](https://github.com/talentchupinchaku/namasthe/tree/main/sample/first_andi)
* You don't have to add ManagedIdentityCredentials or call KeyVault while testing in your local. I will add those to your function. 
* Don't commit your function with password filled in. Leave it empty, and DM me. I will add your password to Azure KeyVault. 
* I marked main branch as protected, please feel free to submit a PR. Create a dummy github account and submit a PR from that to maintain anonymity 
* Add a few lines about what your function does

# documentation 
* You can read more about Azure Functions in their public documentation [here](https://learn.microsoft.com/en-us/azure/azure-functions/) 
