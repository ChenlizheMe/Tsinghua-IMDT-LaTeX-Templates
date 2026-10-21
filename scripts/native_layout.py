"""Measure native Word PDF text geometry; no page raster/PDF backgrounds are used."""
from pathlib import Path
import pdfplumber
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

def num(x):return f'{float(x):.5f}'.rstrip('0').rstrip('.') or '0'

def escape(s):
    return ''.join({'\\':r'\textbackslash{}','{':r'\{','}':r'\}','%':r'\%','$':r'\$','&':r'\&','#':r'\#','_':r'\_','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}.get(c,c) for c in s)

class TextModes(PDFPageAggregator):
    def render_string(self,textstate,seq,ncs,graphicstate):
        self.mode=textstate.render
        return super().render_string(textstate,seq,ncs,graphicstate)
    def render_char(self,matrix,font,fontsize,scaling,rise,cid,ncs,graphicstate):
        self.items.append({'matrix':matrix,'mode':self.mode,'stroke':graphicstate.linewidth})
        return super().render_char(matrix,font,fontsize,scaling,rise,cid,ncs,graphicstate)

def read_pages(path):
    result=[]
    resources=PDFResourceManager()
    device=TextModes(resources)
    interpreter=PDFPageInterpreter(resources,device)
    with Path(path).open('rb') as source,pdfplumber.open(path) as doc:
        for page,p in zip(PDFPage.get_pages(source),doc.pages):
            device.items=[]
            interpreter.process_page(page)
            assert len(device.items)==len(p.chars),(p.page_number,len(device.items),len(p.chars))
            chars=[]
            for c,state in zip(p.chars,device.items):
                assert max(abs(a-b) for a,b in zip(c['matrix'],state['matrix']))<.001
                chars.append(dict(c,render_mode=state['mode'],text_stroke=state['stroke']))
            result.append({'number':p.page_number,'width':p.width,'height':p.height,'chars':chars,'rects':p.rects,'images':p.images})
    return result

FONTS={'SimSun':'song','SimHei':'hei','TimesNewRomanPSMT':'times','TimesNewRomanPS-BoldMT':'timesbold','TimesNewRomanPS-ItalicMT':'timesitalic','SymbolMT':'song','KaiTi':'kai','ArialMT':'arial','Arial-BoldMT':'arialbold','DengXian':'deng','FangSong':'fs'}

def rgb(color):
    if isinstance(color,(float,int)):color=[color]
    if len(color)==1:color=list(color)*3
    assert len(color)==3,color
    return ','.join(num(x) for x in color)

def render_chars(chars):
    runs=[]
    for c in chars:
        if c['text'].isspace():continue
        font=c['fontname'].split('+')[-1]
        style=FONTS[font]
        text=r'\IMDTWordSymbolRoot{}' if font=='SymbolMT' else escape(c['text'])
        stroke=c['text_stroke']/c['size']*100 if c['render_mode'] in (1,2,5,6) else 0
        color=rgb(c['non_stroking_color'])
        x,y=c['matrix'][4:6]
        key=(style,round(c['size'],4),round(y,4),color,round(stroke,3))
        if runs and runs[-1]['key']==key:runs[-1]['chars'].append((x,text))
        else:runs.append({'key':key,'x':x,'y':y,'chars':[(x,text)]})
    result=[]
    for r in runs:
        style,size,y,color,stroke=r['key']
        glyphs=''.join(r'\IMDTGlyph{'+num(x-r['x'])+'}{'+s+'}' for x,s in r['chars'])
        result.append(r'\IMDTWordRun{'+num(r['x'])+'}{'+num(y)+'}{'+style+'}{'+num(size)+'}{'+color+'}{'+num(stroke)+'}{'+glyphs+'}')
    return '\n'.join(result)

def render_rects(rects):
    lines=[]
    for r in rects:
        assert r['fill'] and not r['stroke'],'Unhandled stroked rectangle'
        lines.append(r'\IMDTWordRect{'+num(r['x0'])+'}{'+num(r['y0'])+'}{'+num(r['width'])+'}{'+num(r['height'])+'}{'+rgb(r['non_stroking_color'])+'}')
    return '\n'.join(lines)

def capture_group(chars,text):
    sequence='';indices=[]
    for i,c in enumerate(chars):
        if c['text'].isspace():continue
        sequence+=c['text'];indices.extend([i]*len(c['text']))
    start=sequence.index(text)
    return set(indices[start:start+len(text)])
