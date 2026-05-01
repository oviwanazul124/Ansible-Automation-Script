# Ansible Automation Script

This script made in python is an automation script oriented to be used along side ansible. Eases the configuration of SSH and make it easier to deploy playbooks.

## Basic Configuration

The configuration is made via the `config.ini` here you can set up the:

- `Net Range / Subnet` - This option will allow the script to know where to search the devices that is going to be connecting to.

- `Remote User` - This will be the user that is going to be used when accesing via SSH on Ansible. 

### Requirements

---

This has been tested out on Ubuntu Server with multiples Ubuntu Clients, I don't know if it will work out correctly on other distros (it should work) or even on Windows. If I have spare time I will test it out and update the table

| OS | Supported |
|----|-----------|
|Ubuntu|Supported|

## Different modes

Right now the script has three options:

- `Run Inventory Script` - This options will give you the output of the devices that has been found on the net, this works out as a debug option to test out and see if the range of IPs selected on the `config.ini` is correctly configured.

- `Deploy SSH Key` - This option will deploy the public SSH of the device running to the devices found in net, this is made to not be requiring to verify the authencity of the host. For this to work is necessary to have configured correctly the remote user on the `config.ini`

- `Install Required Packages` - This option will install the packages that are defined in the `AppInstall.yml` on the `playbooks` folder

## Future Updates

I consider this as a final version of the script, but something I may add if I have spare time are:

- Custom running playbooks on the `Install Required Packages`, ask or point via `config.ini` the folder where all the playbooks of the user are, and what wants to be executed

- A bit of reworking of the menu, adding submenu and renaming categories for more easier navigation.