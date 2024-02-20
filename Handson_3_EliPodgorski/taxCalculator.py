#!/usr/bin/env python
# coding: utf-8

# In[ ]:


taxRate= 0.06
def calcSalesTax(total):
    return round(total * taxRate, 2)

def calcTotalAfterTax(total):
    tax = calcSalesTax(total)
    return round(total + tax, 2)


