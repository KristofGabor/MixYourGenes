from django.shortcuts import render
from GeneTest.nucleus import *
from GeneTest import pedigree
from GeneTest.models import *
from django.shortcuts import render
from home.forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User
from home.models import UserProfileInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

global generations
generations={}


@login_required
def index(request):
    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        user_traits=have.objects.filter(user_id=user)
        if len(user_traits)>0:
            results=tests.objects.filter(user_id1=user)
            results=results.union(tests.objects.filter(user_id2=user))
            print(results)
            #here's going to be some history, previous tests
            return render(request,'GeneTest/index.html',{'results':results})
        else:
            traits=trait.objects.all()
            genes={}
            for i in traits:
                genes[i]=gene.objects.filter(trait_name=i)
            print(genes)
            return render(request,'GeneTest/gene_registration.html',{'genes':genes})
@login_required
def TraitDeseaseTest(request,user1=None,user2=None):
    test_types={'Trait test':'trait','Desease test':'desease','Alltogether':'all'}
    if request.method=='POST':
        user1=User.objects.get(username=request.user.username)
        user1=UserProfileInfo.objects.get(user=user1)
        user2=User.objects.get(username=request.POST.get('User2',False))
        user2=UserProfileInfo.objects.get(user=user2)
        test_name=test_types[request.POST.get('test_type',False)]
        context=run(user1,user2,test_name)
        if user1.sex==user2.sex:
            return HttpResponse('Gays can\'t have children, sorry!')
        else:
            print(context)
            TEST={}
            TEST['test']=context['test']
            TEST['figure']=context['figure']
            TEST['result']=context['result']
            TEST['recombination']=recombination.objects.filter(test_id=context['test'])
            return render(request,'GeneTest/results.html',TEST)
    else:
        return HttpResponse('???')

@login_required
def SelfTest(request):
    if request.method=='POST':
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        mom=request.POST.get('mom')
        dad=request.POST.get('dad')
        user1=User.objects.get(username=mom)
        user1=UserProfileInfo.objects.get(user=user1)
        user2=User.objects.get(username=dad)
        user2=UserProfileInfo.objects.get(user=user2)
        test_name='trait'
        context=run(user1,user2,test_name)
        if user1.sex==user2.sex:
            return HttpResponse('Gays can\'t have children, sorry!')
        else:
            print(context)
            TEST={}
            TEST['test']=context['test']
            TEST['figure']=context['figure']
            TEST['result']=context['result']
            TEST['recombination']=recombination.objects.filter(test_id=context['test'])
            #t=tests.objects.get(test_id=TEST['test'].test_id)
            TEST['test'].accessor=user
            TEST['test'].save()
            return HttpResponseRedirect('/account/profile/')
    else:
        return HttpResponse('???')

@login_required
def result(request,test_id):
    if request.method=='GET':
        TEST={}
        TEST['test']=tests.objects.get(test_id=test_id)
        TEST['figure']=figure.objects.get(test_id=TEST['test'])
        TEST['result']=figure.objects.get(test_id=TEST['test'])
        TEST['recombination']=recombination.objects.filter(test_id=TEST['test'])
        print(TEST)
        return render(request,'GeneTest/results.html',TEST)
@login_required
def delete(request,test_id):
    if request.method=='GET':
        t=tests.objects.get(test_id=test_id)
        t.delete()
        return render(request,'account/index.html',{})
@login_required
def gene_registration(request):
    if request.user.is_authenticated:
        user=User.objects.get(username=request.user.username)
        user=UserProfileInfo.objects.get(user=user)
        if request.method=='POST':
            for i in request.POST:
                if i!='csrfmiddlewaretoken' and i!='blank':
                    try:
                        h=have.objects.create(user_id=user, gene_name=gene.objects.get(NCIB_ID=request.POST.get(i)))
                        h.save()
                    except:
                        pass
            return render(request,'GeneTest/index.html',{})


#----------------------PEDIGREE PART -----------------------------------------------



def get_child(object):
    if object.sex:
        ch=type(object).objects.filter(dad=object)
    else:
        ch=type(object).objects.filter(mom=object)
    if len(ch)>0:
        return ch
    else:
        return None

def get_other_parent(object):
    GT=get_child(object)
    if GT is not None:
        if object.sex:
            return GT[0].mom
        else:
            return GT[0].dad
    else:
        return None

def FindFirstGeneration(UserObject):
    if (UserObject.mom is not None) and (UserObject.dad is not None):
        return FindFirstGeneration(UserObject=UserObject.mom),FindFirstGeneration(UserObject=UserObject.dad)
    elif (UserObject.mom is None) and (UserObject.dad is not None):
        return FindFirstGeneration(UserObject=UserObject.dad)
    elif (UserObject.mom is not None) and (UserObject.dad is None):
        return FindFirstGeneration(UserObject=UserObject.mom)
    else:
        return OrderAllGenerations(0,UserObject)

def OrderAllGenerations(index,UserObject):
    global generations
    child=get_child(UserObject)
    if child is not None:
        if index in generations.keys():
            if child[0] not in generations[index]:
                generations[index].append(child[0])
        else:
            generations[index]=[child[0]]
        for i in child:
            return OrderAllGenerations(index+1,i)
    else:
        generations[10000]=[UserObject]
        return generations

def QueryToParentObject(QueryObject, CarriedGene,list):
    return pedigree.Parent(doesHave=pedigree.DoesMemberHave(list,QueryObject.user.username),desease=CarriedGene,sex=QueryObject.sex,ID=QueryObject.user.username)

@login_required
def DrawPedigree(request,gene_id=None,username=None):
    global generations
    generations={}
    subfamily={}
    user=User.objects.get(username=request.user.username)
    user=UserProfileInfo.objects.get(user=user)
    context=FindFirstGeneration(user)
    while isinstance(context,dict) is False:
        context=list(context).pop()
    traits=trait.objects.filter(type='desease')
    genes=[]
    for i in traits:
        genes.append(gene.objects.get(trait_name=i))
    if (username is not None) and (gene_id is not None):
        generations={}
        subfamily2={}
        user2=User.objects.get(username=username)
        user2=UserProfileInfo.objects.get(user=user2)
        context2=FindFirstGeneration(user2)
        while isinstance(context2,dict) is False:
            context2=list(context2).pop()
        desease=gene.objects.get(NCIB_ID=gene_id)
        DeseaseCarrier=have.objects.filter(gene_name=desease)

        GeneOfDesease=pedigree.Gene(intheritance=desease.trait_name.inheritance,name=desease.NCIB_ID,is_X_linked=desease.IsXLinked)
        DoesHaveList=[i.user_id.user.username for i in DeseaseCarrier]
        FamilyMembers={'user1':[],'user2':[]}
        user1=context
        user2=context2
        #user1.pop(10000)
        #user2.pop(10000)
        USERS={'user1':user1, 'user2':user2}
        for user in USERS.keys():
            FamilyMembers[user]=[]
            for i in USERS[user].keys():
                for j in USERS[user][i]:
                    if len(FamilyMembers[user])==0:
                        u=QueryToParentObject(j,GeneOfDesease,DoesHaveList)
                        u.add_dad(QueryToParentObject(j.dad,GeneOfDesease,DoesHaveList))
                        u.add_mom(QueryToParentObject(j.mom,GeneOfDesease,DoesHaveList))
                        FamilyMembers[user].append(u)
                    else:
                        u=QueryToParentObject(j,GeneOfDesease,DoesHaveList)
                        for i in FamilyMembers[user]:
                            if i.ID == j.dad.user.username:
                                u.add_dad(i)
                            if i.ID == j.mom.user.username:
                                u.add_mom(i)
                        if u.mom is None:
                            u.add_mom(QueryToParentObject(j.mom,GeneOfDesease,DoesHaveList))
                        if u.dad is None:
                            u.add_dad(QueryToParentObject(j.mom,GeneOfDesease,DoesHaveList))
                        FamilyMembers[user].append(u)
        print(FamilyMembers['user1'][3].dad.dad.ID)
        return render(request,'GeneTest/pedigree.html',{'UserFamily':context, 'PartnerFamily':context2,'genes':genes, 'carrier':DeseaseCarrier})
    else:
        return render(request,'GeneTest/pedigree.html',{'UserFamily':context, 'genes':genes})
