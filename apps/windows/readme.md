## APP说明

> winRM 服务是 windows server下 PowerShell 的远程管理服务。Python 脚本通过连接 winRM 模块操作 windows 命令行。

## 开启 winRM 服务

> 不要忘记设置防火墙

```
查看 winRM 服务状态，默认都是未启动状态
> winrm e winrm/config/listener

winRM 服务启动
> winrm quickconfig

为 winrm service 配置 auth
> winrm set winrm/config/service/auth "@{Basic="true"}"

为 winrm service 配置加密方式为允许非加密
> winrm set winrm/config/service "@{AllowUnencrypted="true"}"
```

## 动作列表

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **host**  | text | `是` | 主机地址 |
| **port**  | number | `是` | 端口 |
| **user**  | text | `是` | 登录用户 |
| **passwd**  | text | `是` | 登录密码 |
| **cmd**  | text | `是` | 执行命令 |

**返回值：**

```
执行命令的返回结果
```