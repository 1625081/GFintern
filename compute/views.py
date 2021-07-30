import numpy
import scipy

from django.http import Http404

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Computation, Operation

#Tools Function
def str2num(LineString,comment='#'):
 
    from io import StringIO as StringIO
    import re,numpy
 
    NumArray=numpy.empty([0],numpy.int16)
    NumStr=LineString.strip()
    #~ ignore comment string
    for cmt in comment:
        CmtRe=cmt+'.*$'
        NumStr=re.sub(CmtRe, " ", NumStr.strip(), count=0, flags=re.IGNORECASE)
 
    #~ delete all non-number characters,replaced by blankspace.
    NumStr=re.sub('[^0-9.e+-]', " ", NumStr, count=0, flags=re.IGNORECASE)
 
    #~ Remove incorrect combining-characters for double type.
    NumStr=re.sub('[.e+-](?=\s)', " ", NumStr.strip(), count=0, flags=re.IGNORECASE)
    NumStr=re.sub('[.e+-](?=\s)', " ", NumStr.strip(), count=0, flags=re.IGNORECASE)
    NumStr=re.sub('[e+-]$', " ", NumStr.strip(), count=0, flags=re.IGNORECASE)
    NumStr=re.sub('[e+-]$', " ", NumStr.strip(), count=0, flags=re.IGNORECASE)
 
    if len(NumStr.strip())>0:
        StrIOds=StringIO(NumStr.strip())
        NumArray= numpy.genfromtxt(StrIOds)
 
    return NumArray

# 重新获取保存为str的NUMPY数组的方式
# from io import StringIO
# m = Compute.matrix_1
# m_neo=re.sub("[\[\]]","",m.strip(),flags=re.IGNORECASE)
# numpy.loadtxt(StringIO(m_neo))

def index(request):
    latest_computes_list = Computation.objects.all()
    context = {
        'latest_computes_list': latest_computes_list,
    }
    return render(request, 'compute/index.html', context)

def add(request):
    try:
        op = request.POST['operation']
        matrix_1 = request.POST['matrix_1']
        matrix_2 = request.POST['matrix_2']
        lines_num = max(len(matrix_1.split(";")), len(matrix_1.split("\n")))
        m_1 = str2num(matrix_1)
        m_2 = str2num(matrix_2)
        m_1 = m_1.reshape((lines_num,int(m_1.size/lines_num)))
        m_2 = m_2.reshape((lines_num,int(m_2.size/lines_num)))
        if op=='sum':
            re = m_1 + m_2
        elif op=='mul':
            re = numpy.matmul(m_1, m_2)
        #selected_operation = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Operation.DoesNotExist):
        return render(request, 'compute/detail.html', {
            'compute': compute,
            'error_message': "You didn't select a choice.",
        })
    else:
        compute = Computation(matrix_1=m_1, matrix_2=m_2, result=re)
        compute.save()
        cop = compute.operation_set.create(op_text=op)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('compute:results', args=(compute.id,cop.id)))

def detail(request, compute_id):
    compute = get_object_or_404(Computation,pk=compute_id)
    return render(request, 'compute/detail.html', {'compute': compute})

def results(request, compute_id, cop_id):
    compute = get_object_or_404(Computation, pk=compute_id)
    op = compute.operation_set.get(pk=cop_id)
    return render(request, 'compute/results.html', {'compute': compute,'op': op})

def vote(request, compute_id):
    compute = get_object_or_404(Computation, pk=compute_id)
    try:
        op = request.POST['operation']
        matrix_1 = request.POST['matrix_1']
        matrix_2 = request.POST['matrix_2']
        m_1 = str2num(matrix_1)
        m_2 = str2num(matrix_2)
        lines_num = max(len(matrix_1.split(";")), len(matrix_1.split("\n")))
        m_1 = str2num(matrix_1)
        m_2 = str2num(matrix_2)
        m_1=m_1.reshape((lines_num,int(m_1.size/lines_num)))
        m_2=m_2.reshape((lines_num,int(m_2.size/lines_num)))
        if op=='sum':
            re = m_1 + m_2
        elif op=='mul':
            re = numpy.matmul(m_1, m_2)
        #selected_operation = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Operation.DoesNotExist):
        return render(request, 'compute/detail.html', {
            'compute': compute,
            'error_message': "You didn't select a choice.",
        })
    else:
        temp_op = compute.operation_set.get(pk=1)
        temp_op.op_text = op
        temp_op.save()
        compute.result = re
        compute.matrix_1 = m_1
        compute.matrix_2 = m_2
        compute.save()
        #selected_choice.votes += 1
        #selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('compute:results', args=(compute.id,temp_op.id)))