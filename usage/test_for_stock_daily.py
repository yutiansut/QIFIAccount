#!/usr/bin/env python
# coding: utf-8

# In[53]:


import QIFIAccount


# In[54]:


acc =  QIFIAccount.QAQIFIAccount.QIFI_Account(username='ax', password='ax',model="BACKTEST")


# In[55]:


acc.initial()


# In[56]:


order = acc.send_order('000001', 100, 12, QIFIAccount.ORDER_DIRECTION.BUY, datetime='2020-01-01')


# In[57]:


acc.make_deal(order)


# In[58]:


pos = acc.get_position('000001')


# In[59]:


acc.on_price_change('000001', 12.3, '2020-01-01 11:22:00')


# In[60]:


pos = acc.get_position('000001')


# In[61]:


print(pos.realtime_message)


# In[62]:


acc.balance


# In[63]:


acc.settle()


# In[64]:


acc.balance


# In[65]:


pos = acc.get_position('000001')


# In[66]:


print(pos.realtime_message)


# In[67]:


acc.on_price_change('000001', 12.3, '2020-01-02 09:32:00')


# In[68]:


pos.message


# In[69]:


order = acc.send_order('000001', 100, 12.3, QIFIAccount.ORDER_DIRECTION.SELL, datetime='2020-01-02')


# In[70]:


pos = acc.get_position('000001')


# In[72]:


pos.message


# In[43]:


order


# In[44]:


acc.make_deal(order)


# In[45]:


acc.trades


# In[46]:


pos = acc.get_position('000001')


# In[51]:


pos.message


# In[52]:


pos.volume_long


# In[48]:


pos.realtime_message


# In[50]:


acc.positions


# %%
acc.message
# %%
