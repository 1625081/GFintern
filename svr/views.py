import numpy
import scipy,os
import matlab.engine
from django.http import Http404

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import SVRmodel

# 重新获取保存为str的NUMPY数组的方式
# from io import StringIO
# m = Compute.matrix_1
# m_neo=re.sub("[\[\]]","",m.strip(),flags=re.IGNORECASE)
# numpy.loadtxt(StringIO(m_neo))

def index(request):
	
    return render(request, 'svr/index.html')

def add(request):
    if request.method == "POST":
        xlsx_share = request.FILES.get('share',None)
        xlsx_fund = request.FILES.get('fund',None)
        if not xlsx_share:
            return HttpResponse("No files Uploaded!")
        dst_1 = open(os.path.join("C:\\Users\\sanjin\\GFdb\\GFdb\\SVR\\Upload\\",xlsx_share.name),'wb')
        for chunk in xlsx_share.chunks():
            dst_1.write(chunk)
        dst_1.close()
        dst_2 = open(os.path.join("C:\\Users\\sanjin\\GFdb\\GFdb\\SVR\\Upload\\",xlsx_fund.name),'wb')
        for chunk in xlsx_fund.chunks():
            dst_2.write(chunk)
        dst_2.close()
        share_addr = os.path.join("C:\\Users\\sanjin\\GFdb\\GFdb\\SVR\\Upload\\",xlsx_share.name)
        fund_addr = os.path.join("C:\\Users\\sanjin\\GFdb\\GFdb\\SVR\\Upload\\",xlsx_fund.name)
        model = SVRmodel(share_addr=share_addr,fund_addr=fund_addr,mse="0",mae="0")
        model.save()
        return HttpResponseRedirect(reverse('svr:results', args=(model.id,)))

def detail(request, svr_id):
    model = get_object_or_404(SVRmodel,pk=svr_id)
    return render(request, 'SVR/detail.html', {'model': model})

def results(request, svr_id):
    model = get_object_or_404(SVRmodel, pk=svr_id)
    eng = matlab.engine.start_matlab()
    share_addr = model.share_addr
    fund_addr = model.fund_addr
    mse,mae = eng.svr_core(share_addr,fund_addr,nargout=2)
    model.mse = str(mse)
    model.mae = str(mae)
    model.save()
    return HttpResponse("Success!")
