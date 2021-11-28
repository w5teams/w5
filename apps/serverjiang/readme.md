## APP 说明

> 不要忘记绑定微信,否则无法通知

- 官方文档：http://sc.ftqq.com/

## 动作列表

### 微信通知

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **key**  | text | `是` | Server酱 Key，登录账号后可以看到 |
| **text**  | text | `是` | 通知标题 |
| **desp**  | text | `否` | 通知内容|

**返回值：**

```
# 正常
{'errno': 0, 'errmsg': 'success', 'dataset': 'done'}
```