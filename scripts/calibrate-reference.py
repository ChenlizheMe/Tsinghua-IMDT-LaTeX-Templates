from pathlib import Path
import shutil
from pypdf import PdfReader
from native_layout import read_pages,render_chars,render_rects,capture_group,num

import argparse
parser=argparse.ArgumentParser(description="Rebuild native layout data from Microsoft Word PDF exports")
parser.add_argument('--form-pdf',type=Path,required=True)
parser.add_argument('--report-pdf',type=Path,required=True)
args=parser.parse_args()
REPO=Path(__file__).resolve().parents[1]

def value(x,y,w,size,macro):
    return r'\IMDTWordValue{'+num(x)+'}{'+num(y)+'}{'+num(w)+'}{'+num(size)+'}{'+macro+'}'

def default_text(chars,text,macro,default,x,y,w,size):
    ids=capture_group(chars,text)
    native=render_chars([c for i,c in enumerate(chars) if i in ids])
    return ids,r'\ifdefstrequal{'+macro+'}{'+default+'}{%\n'+native+'%\n}{'+value(x,y,w,size,macro)+'}'

def group_where(chars,predicate):return {i for i,c in enumerate(chars) if predicate(c)}

def conditional_group(chars,ids,test,override):
    native=render_chars([c for i,c in enumerate(chars) if i in ids])
    return test+'{%\n'+native+'%\n}{'+override+'}'

def area(x,y,w,h,macro):
    return r'\IMDTWordArea{'+num(x)+'}{'+num(y)+'}{'+num(w)+'}{'+num(h)+'}{'+macro+'}'

form=read_pages(args.form_pdf)
names=['cover','topic-literature','assessment','work-plan']
layout=REPO/'forms/layout'
layout.mkdir(exist_ok=True)
for p,name in zip(form,names):
    chars=p['chars'];skip=set();extra=[]
    if p['number']==1:
        for text,macro,default,x,y,w in [
            ('深圳国际研究生院',r'\SchoolName',r'\IMDTDefaultSchoolName',158.69,330.17,264.05),
            ('电子信息（互动媒体设计与技术）',r'\MajorName',r'\IMDTDefaultMajorName',163.97,283.25,258.05)]:
            ids,code=default_text(chars,text,macro,default,x,y,w,12);skip|=ids;extra.append(code)
        ids=group_where(chars,lambda c:c['matrix'][5]<100)
        skip|=ids
        extra.append(conditional_group(chars,ids,r'\ifdefstrequal{\FormDate}{\IMDTDefaultFormDate}',value(180,81.42,162,12,r'\FormDate')))
        for r,macro in zip([p['rects'][i] for i in [0,1,4,5,6]],[r'\StudentName',r'\StudentID',r'\Supervisor',r'\SupervisorRank',r'\EnrollmentDate']):
            extra.append(value(r['x0'],r['y0']+2.4,r['width'],12,macro))
    elif p['number']==2:
        for idx,macro in zip([0,1,2,3],[r'\IMDTFormTitle',r'\TopicScope',r'\ClassificationNumber',r'\CrossDisciplineName']):
            r=p['rects'][idx];extra.append(value(r['x0'],r['y0']+1.68,r['width'],10.56,macro))
        extra.extend([value(132.02,299.93,63.02,10.56,r'\DomesticReferenceCount'),value(279.07,299.93,89.18,10.56,r'\ForeignReferenceCount')])
        ids=group_where(chars,lambda c:abs(c['matrix'][5]-544.18)<.3 and c['x0']>160 and c['text'] in '年月日')
        assert len(ids)==3,(ids,[(c['text'],c['matrix'][5]) for c in chars if c['text'] in '年月日'])
        skip|=ids
        extra.append(conditional_group(chars,ids,r'\ifdefstrequal{\ProposalMeetingDate}{\IMDTDefaultMeetingDate}',value(165,544.18,185,10.56,r'\ProposalMeetingDate')))
        extra.append(area(47.88,268,420,165,r'\KeyReferences'))
    elif p['number']==3:
        extra.append(area(47.88,560,420,72,r'\AdvisorComment'))
    else:
        extra.extend([area(47.88,600,420,32,r'\ResearchConditions'),area(47.88,458,420,30,r'\ProjectCategory'),area(47.88,320,420,130,r'\MainWorkPlan')])
        for x,y,w,macro in [(216.29,156.98,246.67,r'\LiteratureCompletionDate'),(184.85,139.34,278.11,r'\ResearchCompletionDate'),(163.73,121.7,299.23,r'\WritingCompletionDate'),(374.74,353.45,73.44,r'\OtherTypeDescription')]:
            extra.append(value(x,y,w,10.56,macro))
        for i,macro in enumerate([r'\TypeResearch',r'\TypeCase',r'\TypeScheme']):extra.append(value(43,387.79-17.17*i,40,10.56,macro))
        for i,macro in enumerate([r'\TypeSurvey',r'\TypeProduct',r'\TypeOther']):extra.append(value(227.1,387.79-17.17*i,42,10.56,macro))
    if p['number'] in (2,4):
        cc=[c for c in chars if not c['text'].isspace()]
        pairs=[(c,cc[i+1]) for i,c in enumerate(cc[:-1]) if c['text'] in ('（','(') and cc[i+1]['text'] in ('）',')')]
        macros=[r'\PublicMark',r'\SecretMark',r'\ConfidentialMark',r'\CrossYes',r'\CrossNo',r'\ExpertYes',r'\ExpertNo'] if p['number']==2 else [r'\ExperimentYes',r'\ExperimentNo',r'\TrainingYes',r'\TrainingNo',r'\SafetyReportYes',r'\SafetyReportNo']
        assert len(pairs)==len(macros)+1
        for (left,right),macro in zip(pairs[1:],macros):
            x=left['x1'];w=right['x0']-x
            extra.append(value(x,left['matrix'][5],w,10.56,macro))
    static=render_chars([c for i,c in enumerate(chars) if i not in skip])
    code='% 原 Word 固定版式；文字为原生 TeX，填写值在配置文件中维护。\n'+render_rects(p['rects'])+'\n'+static+'\n% 可填写字段\n'+'\n'.join(extra)+'\n'
    (layout/f'{name}.tex').write_text(code.rstrip()+chr(10),encoding='utf-8')
    (REPO/'forms'/f'{name}.tex').write_text('% !TeX root = ../imdt-topic-work-plan.tex\n'+r'\IMDTWordPage{forms/layout/'+name+'}\n',encoding='utf-8')

report=read_pages(args.report_pdf)
layout=REPO/'reference-layout'
layout.mkdir(exist_ok=True)
image=PdfReader(args.report_pdf).pages[7].images[0]
imagepath=REPO/'figures/original-route-example.png'
image.image.save(imagepath)
for p in report:
    chars=p['chars'];skip=set();extra=[]
    if p['number']==2:
        for text,macro,default,x,y,w,size in [
            ('深圳国际研究生院',r'\SchoolName',r'\IMDTDefaultSchoolName',259.85,414.31,160,15.96),
            ('电子信息（互动媒体设计与技术）',r'\MajorName',r'\IMDTDefaultMajorName',258.05,381.53,240,15.96)]:
            ids,code=default_text(chars,text,macro,default,x,y,w,size);skip|=ids;extra.append(code)
        ids=group_where(chars,lambda c:abs(c['matrix'][5]-612.34)<.1)
        skip|=ids
        title_value=value(89.88,612.34,415.6,21.96,r'\ThesisTitle').replace('IMDTWordValue','IMDTWordTitleValue')
        extra.append(conditional_group(chars,ids,r'\ifdefstrequal{\ThesisTitle}{\IMDTDefaultTitle}',title_value))
        ids=group_where(chars,lambda c:abs(c['matrix'][5]-134.42)<.1)
        skip|=ids
        extra.append(conditional_group(chars,ids,r'\ifdefstrequal{\ReportDate}{\IMDTDefaultReportDate}',value(197.66,134.42,200,15.96,r'\ReportDate')))
        ids=group_where(chars,lambda c:abs(c['matrix'][5]-283.25)<.1 and c['x0']>270)
        skip|=ids
        extra.append(conditional_group(chars,ids,r'\ifdefempty{\Supervisor}',value(258.05,283.25,240,15.96,r'\Supervisor')))
        extra.extend([value(258.05,348.77,240,15.96,r'\StudentName'),value(258.05,316.01,240,15.96,r'\StudentID')])
    images='\n'.join(r'\IMDTWordImage{'+num(i['x0'])+'}{'+num(i['y0'])+'}{'+num(i['width'])+'}{'+num(i['height'])+'}{figures/original-route-example.png}' for i in p['images'])
    code='% 原 Word 第 '+str(p['number'])+' 页；原生 TeX 文字与规则线。\n'+render_rects(p['rects'])+'\n'+images+'\n'+render_chars([c for i,c in enumerate(chars) if i not in skip])+'\n'+'\n'.join(extra)+'\n'
    (layout/f'page-{p["number"]:02}.tex').write_text(code.rstrip()+chr(10),encoding='utf-8')
print('Generated native form (4 pages) and complete report reference (12 pages).')
