import env
from pop3_handle import POP3_

a = POP3_(env.email, env.password)

flag = a.checkMailBoxNotNull()
print(f"Mailbox not null?: {flag}")
if flag:
    info = a.getTopMail()
    print(info)


a.closeConnection()

