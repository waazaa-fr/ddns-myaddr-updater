**ddns-myaddr-updater**

Docker image on Docker HUB: https://hub.docker.com/r/waazaafr/ddns-myaddr-updater



This is a simple client to update DNS entries offered by https://myaddr.tools (thx to him).


You must create a config.yml containing your configuration for multiple updates.

Example of config.yml:
```yml
example1.myaddr.tools:
  KEY: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  IPv4: auto
  IPv6: "fe80::1"
  NO_UPDATE_LIMIT: 30
example2.myaddr.tools:
  KEY: YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
  IPv4: auto
  IPv6: none
  NO_UPDATE_LIMIT: 30
```

In this example "example1.myaddr.tools" is just a name easy to remember for you for logging purpose only.



**KEY** is the myaddr.tools API KEY obtained by claiming a subdomain.


For **IPv4** and **IPv6** you can choose between:
- **auto** - ip is updated if changed retrieved using https://api.ipify.org for ipv4 and https://api64.ipify.org for ipv6
- **xxxx** - you set a fixed ip yourself
- **none** - no POST API call for it


**NO_UPDATE_LIMIT** is the number of day between 2 POST API call if ip is unchanged a force call is done.


Each config node is launched every 15 mn.


**Docker run**

```bash
docker run -it --rm --name ddns-myaddr v /mnt/user/appdata/ddns-myaddr-updater:/config waazaafr/ddns-myaddr-updater:latest
```

In this run command /mnt/user/appdata/ddns-myaddr-updater must contains config.yml