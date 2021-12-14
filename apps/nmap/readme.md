## APP说明

**本机需要安装 nmap 工具**

## 动作列表

### 端口扫描

**参数**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **target**  | text | `是` | IP 或 域名 |
| **ports**  | text | `是` | 端口类别，多个英文逗号分隔，列如 80,8888,8081 |
| **protocol**  | text | `是` | tcp 或 udp 协议 |

**返回值：**

```
返回 json 数据
{'107.36.113.181': {'hostnames': [{'name': 'wwwww.io', 'type': 'user'}], 'addresses': {'ipv4': '101.36.113.187'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'syn-ack'}, 'tcp': {21: {'state': 'filtered', 'reason': 'no-response', 'name': 'ftp', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '8.0', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/a:openbsd:openssh:8.0'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'nginx', 'version': '1.14.1', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:igor_sysoev:nginx:1.14.1'}, 2222: {'state': 'filtered', 'reason': 'no-response', 'name': 'EtherNetIP-1', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 3306: {'state': 'filtered', 'reason': 'no-response', 'name': 'mysql', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 8081: {'state': 'filtered', 'reason': 'no-response', 'name': 'blackice-icecap', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}}}}
```