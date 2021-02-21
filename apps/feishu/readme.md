## APP 说明

- 飞书官方文档：https://www.feishu.cn/hc/zh-CN/articles/360024984973

## 动作列表

### 飞书通知

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **hook_uuid**  | text | `是` | URL hook 后面的 UUID |
| **msg**  | text | `是` | 通知内容|

**返回值：**

```
# 正常
{'Extra': None, 'StatusCode': 0, 'StatusMessage': 'success'}
```