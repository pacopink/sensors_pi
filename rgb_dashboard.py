#!/bin/python
#coding:utf8
# Paco Li: 2019-04-22
# a client to connect control PWM LED freq and duty_cycle

from Tkinter import *
import redis

r = None
pwm_init_flag = False

window = Tk()
window.title("PWM LED Dashboard")
window.geometry('480x240')

layouts = (
        ('redis host', 'localhost'),
        ('redis port', '6379'),
        ('redis auth', '')
        )

row = 0
labels = dict()
entries = dict()
vars = dict()
for i in layouts:
    print i[0], '-', i[1]
    lb = Label(window, text=i[0])

    v = StringVar(window, value=i[1])
    entry = Entry(window, textvariable=v)

    labels[i[0]] = lb
    entries[i[0]] = entry
    vars[i[0]] = v

    lb.grid(column = 0, row = row)
    entry.grid(column = 1, row = row)
    row +=1


pwm_vars = dict()

def on_update_pwm():
    print "on_update_pwm"
    for k,v in pwm_vars.items():
        r.set(k, v.get())

btnPWM  = Button(window, text="update", command=on_update_pwm)

def init_pwm(keys):
    global row
    for i in keys:
        col = 0
        for j in xrange(0,2):
            key = i[j]
            print key
            val = r.get(key)
            l = Label(window, text=key + (" (Hz)" if j==0 else " (%)"))
            v = StringVar(window, value=val)
            e = Entry(window, textvariable=v)
            l.grid(column=col, row=row)
            col+=1
            e.grid(column=col, row=row)
            col+=1
            pwm_vars[key] = v
        row+=1
    if len(pwm_vars.keys())>0:
        btnPWM.grid(column=0, row=row)
        global pwm_init_flag
        pwm_init_flag = True



def on_config():
    print "on click"
    host = vars['redis host'].get()
    auth = vars['redis auth'].get()
    port = int(vars['redis port'].get())
    print host, port, auth
    global r
    r = redis.Redis(host, port, password = auth if len(auth)>0 else None)
    print r.ping()

    if not pwm_init_flag:
        init_pwm(zip(r.keys('*:freq'), r.keys('*:duty')))


btn = Button(window, text="ok", command=on_config)
btn.grid(column=0, row=row)
row+=1

window.mainloop()
