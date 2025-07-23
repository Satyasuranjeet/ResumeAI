from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import re
from collections import Counter
import tempfile
import sys

# Add the parent directory to the path so we can import from the main app
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))
app.secret_key = 'resume-analyzer-vercel-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Stopwords set (same as your original)
stopwords = {'haven', 'course', 'n', 'io', 'one', 'clearly', 'made', 'resulted', 'pf', 'how', 'ax', 'fifth', 'causes', 'section', 'results', 'ga', 'anyone', 'yl', 'without', 'million', 'fu', 'di', 'hereby', 'au', 'tends', 'eo', 'ca', 'off', 'q', 'wa', 'sixty', 'ci', 'tm', 'bk', 'merely', 'my', 'necessary', 'os', 'thats', 'dx', 'hi', '0o', 'hundred', 'rh', 'therein', 'thereto', 'sd', 'do', 'think', 'taken', "they've", 'f', 'il', "aren't", 'uj', 'though', 'les', 'yes', 'throug', 'associated', 'amoungst', 'seeing', 'way', 'hardly', 'few', 'outside', 'nd', 'wherever', 'inasmuch', 'cant', 'liked', 'but', 'name', 'qv', 'often', 'shows', 'lately', 'quickly', 'widely', 'considering', 'system', 'meanwhile', 'using', 'ourselves', 'mg', 'pp', 'mu', 'keeps', 'truly', 'kg', 'beginnings', 'lb', 'already', 'ep', 'formerly', 'anywhere', 'i7', 'soon', 'hed', 'll', "shouldn't", 'whenever', 'resulting', 'that', 'est', 'aside', 'successfully', 'like', 'hy', 'ib', 'lt', 'promptly', 'we', 'themselves', 'found', 'pages', 'p', 'right', 'og', 'get', 'couldn', 'wo', 'various', "she'll", 'ab', 'whomever', 'ur', "a's", 'wherein', 'anybody', 'came', 'moreover', 'cc', 'ti', 'further', 'hasn', 'before', 'theirs', "where's", 'makes', 'otherwise', 'doing', 'has', 'went', 'ol', 'biol', 'same', 'h', 'yet', 'probably', 'normally', 'anything', 'thereupon', 'cm', 'zz', 'b3', 'come', 'information', 'dd', 'myself', 'proud', 'fy', 'pr', 'bl', 'whereupon', 'inc', "he'd", 'back', 'h3', 'p1', 'nor', 'nowhere', 'across', 'rl', 'showed', "when's", 'by', 'gy', 'put', 'third', 'while', 'far', 'looks', "let's", "mustn't", 'related', 'werent', 'own', 'gets', "c'mon", 's2', 'home', 'ow', 'respectively', 'hh', 'hid', 'dk', 'ml', 'according', 'cl', 'oc', "doesn't", 'ibid', 'ys', "there's", 'tx', 'tr', 'and', 'ain', 'ra', 'mo', 'bt', 'az', 'ju', "here's", 'i3', 'look', 'ns', 'fj', 'jj', 'rj', 'sorry', 'sc', "there'll", 'sz', 'says', 'ought', 'might', 'significantly', 'plus', 'lest', 'usually', 'now', 'seeming', 'don', 'its', 'of', 'regarding', 'were', 'sec', 'thence', 'interest', 'able', 'od', 'happens', 'index', '3a', 'ps', 'useful', 'up', 'b1', 'due', 'find', 'beginning', 'j', 'several', 'amount', 'xj', 'ih', 'every', 'took', 'suggest', 'ff', 'pc', 'lc', 'somethan', "there've", 'since', 'ny', 'bn', 'definitely', 'le', 'al', 'cr', 'ok', 'see', 'somewhere', 'tries', 'ft', 'unfortunately', 'whereas', 'furthermore', 'apparently', 'unless', 's', "won't", 'his', 'xi', 'bs', 'ce', 'sensible', 'y2', 'seriously', 'y', 'dc', 'et-al', 'gr', 'didn', 'act', 'needs', 'comes', 'ours', 'vol', "what'll", 'fill', 'ko', 'tj', 'another', 'affects', 'page', 'weren', 'u', 'afterwards', 'appear', "wasn't", 'only', 'o', 'ss', 'abst', 'ed', 'sincere', 'per', 'jt', 'm2', 'hes', 'presumably', 'fo', 'ox', 'bj', 'shed', 'hello', 'tl', 'also', 'more', 'however', 'amongst', 'along', 'particular', 'slightly', 'whereby', 'describe', 'there', 'better', "wouldn't", "it's", 'whither', 'lr', 'til', 'h2', 'ups', 'bi', 'seemed', 'twenty', 'strongly', 'co', 'none', 'them', "c's", 'or', 'least', 'quite', 'against', 'nonetheless', 'zero', 'mainly', 'end', 'mustn', 'necessarily', 'bx', 'qu', 'obtained', 'tip', 'b', 'eg', 'hasnt', 'whod', 'her', 'know', 'neither', 'pk', 'nevertheless', 'than', 'da', 'elsewhere', 'com', 'yr', "they'd", 'such', 'thereof', 'can', 'thru', 'down', 'edu', 'indicated', 'possible', 'ref', 'thus', 'not', 're', 'dt', 'ie', 'toward', 'announce', 'actually', "i'd", 'hs', 'maybe', 'value', 'av', 'consequently', 'sn', 'pn', 'having', 'apart', 'ue', 'ever', 'thou', 'welcome', 'hers', 'w', 'likely', 'said', 'added', 'vq', 'mn', 'ni', 'anyhow', 'bottom', 'cs', "that've", "t's", 'xs', 'wasnt', 'five', 'pagecount', 'herself', 'rc', 'sq', 'what', "who'll", 'id', 'contains', 'ou', 'xx', 'wasn', 'whereafter', 'whole', 'em', 'does', 'me', "i'm", 'awfully', 'stop', 'beside', 'briefly', 'six', 'ea', 'everyone', 'indicate', 'near', "you'd", 'accordingly', 'goes', 'will', 'did', 'hu', 'exactly', 'corresponding', 'kept', 'nj', 'then', 'ry', 'ho', 'somehow', 'nl', 'wouldn', 'ip', 'novel', 'ask', 'into', 'had', 'cf', 'reasonably', 'l2', 'ro', 'z', 'cj', 'dr', 'cd', 'pd', 'thoughh', 'wonder', 'just', 'el', 'obtain', 'cx', 'willing', 'va', 'ma', 'detail', 'this', 'ot', 'ev', 'ones', 'vs', 'ac', 'concerning', 'cannot', 'fa', 'besides', 'nearly', 'three', 'x', 'a2', 'ending', 'cit', 'shan', 'd2', 'vt', '6b', 'pm', 'poorly', 'for', 'sent', 'yourselves', 'significant', 'oi', 'e', 'research-articl', 'c3', 'shes', 'been', 'e3', 'ej', 'ri', 'theyd', 've', "we'd", 'during', 'cz', 'placed', 'ec', 'v', 'allow', 'showns', 'ap', 'yourself', 'fc', 'certainly', 'best', 'cy', "haven't", 'many', 'tc', 'cp', 'important', 'noted', 'oz', 'op', 'you', 'nt', 'omitted', 'let', 'a4', 'sy', 'on', 't2', 'js', 'es', '3b', 'hereafter', 'gi', 'latter', 'especially', 'refs', 'substantially', 'x2', 'she', 'uk', 'which', 'no', 'km', 'f2', 'ltd', 'td', 'tf', 'ey', 'theyre', 'follows', 'ob', 'fire', 'hither', 'keep', 'next', 'because', 'towards', 'potentially', 'effect', 'rn', 'shouldn', 'nc', 'getting', 'largely', 'always', 'when', 'ct', 'cu', 'ij', 'wont', 'serious', 'lf', 'theres', 'ut', 'i4', 'mean', 'cq', 'cry', 'aw', 'being', 'ls', 'mug', 'our', 'unlike', 'twelve', 'seem', 'after', "should've", 'aren', 'whim', 'i8', 'those', 'to', 'former', "how's", 'iz', 'similarly', 'mightn', "what's", 'hereupon', 'u201d', 'similar', 'where', 'alone', 'later', 'around', 'gives', 'rq', 'else', 'somewhat', 'sure', 'different', 'eq', 'ninety', 'whose', 'om', 'once', 'very', 'yj', 'jr', 'brief', 'youre', 'give', 'vu', 'believe', 'l', "hasn't", 'viz', 'arise', "didn't", 'affected', 'appropriate', 'couldnt', 'ii', 'gave', 'miss', 'about', 'he', 'po', "i'll", 'rr', 'shown', 'xf', 'say', 'therefore', 'los', 'ru', 'fix', 'wouldnt', 'thank', 'i2', 'ph', 'predominantly', 'particularly', 'b2', 'they', 'last', 'eleven', 'these', 'volumtype', 'greetings', 'ar', "he's", 'oq', 'whence', 'trying', 'de', 'tq', 'a3', 'regards', 'second', 'seven', 'out', 'obviously', 'dj', 'sup', 'as', 'date', 'seen', 'usefully', 'xv', 'cv', 'all', "it'd", 'sa', 'vo', 'rather', 'research', 'was', 'doesn', 'provides', 'new', 'sub', 'giving', 'http', 'over', 'du', 'throughout', 'whoever', 'youd', 'less', 'nay', 't3', "you've", 'sp', 'move', 'c', 'hr', 'itd', 'whom', "can't", 'described', 'used', 'gl', "it'll", 'needn', 'p2', 'sufficiently', 'downwards', 'xl', 'xn', 'anyways', 'con', 'te', 'ei', 'ir', 'mill', 'tell', 'whatever', 'howbeit', 'yt', 'empty', 'who', 'specified', 'ae', 'ng', 'rv', 'could', 'am', 'ex', 'still', 'thoroughly', 'ao', "why's", 'onto', 'na', 'immediate', 'n2', 'previously', 'behind', 'okay', 'sometime', 'containing', 'until', 'make', 'became', 'oh', 'etc', 'tb', 'following', 'mostly', 'anymore', 'kj', 'recently', 'tried', 'dl', 'xo', "don't", 'self', 'heres', 'gone', 'top', 'via', 'iy', 'somebody', 'hence', 'rd', 'it', 'begin', 'everywhere', 'ln', 'must', 'whos', 'lets', 'ms', 'unto', 'insofar', 'm', 'forty', 'mine', 'except', 'regardless', 'aj', 'appreciate', 'contain', 'fi', 'mt', 'que', 'thanx', 'a', 'are', 'fs', 'non', 'their', 'becomes', 'nn', 'st', 'namely', 'currently', 'usefulness', 'unlikely', 'adj', 'oa', 'c1', 'may', 'even', 'either', 'latterly', 'call', "they're", 'is', 'wants', 'readily', 'sr', 'i', 'show', 'wish', 'i6', 'certain', 'well-b', 'eu', '3d', 'dy', 'ia', 'nos', 'fl', 'something', 'try', 'e2', 'noone', 'g', 'qj', 'thorough', 'above', 'accordance', 'vj', 'ui', 'um', 'everybody', 'us', 'ds', 'ay', "couldn't", 'recent', 'selves', 'upon', 'done', 'et', 'other', "we're", "we'll", 'becoming', 'two', 'anyway', 'tt', 'tv', 'sj', 'un', 'saw', 'from', 'have', 'importance', 'given', 'sm', 'little', 'gj', 'mr', 'ts', 'x3', "ain't", 'br', 'meantime', 'eight', 'hopefully', 'ne', 't', "he'll", 'si', 'front', 'the', 'vd', 'why', 'any', 'df', 'zi', 'allows', 'ix', 'line', 'whats', 'r2', 'so', 'ag', 'changes', 'uses', 'present', 'overall', 'ten', 'within', "you're", 'below', 'inward', 'thanks', 'side', 'k', 'sometimes', 'help', 'er', 'everything', 'got', 'bu', 'rf', 'vols', 'ad', 'use', 'hadn', 'thered', 'with', 'would', 'him', 'nothing', 'par', 'here', 'sl', 'pq', 'too', 'won', 'someone', 'fifteen', 'pl', 'away', 'each', "they'll", 'followed', 'in', 'possibly', 'consider', 'begins', 'indeed', 'owing', 'going', 'ee', 'relatively', 'cn', 'iq', 'old', 'lo', 'cause', 'run', 'www', 'part', 'pt', "needn't", 'mrs', 'seems', 'words', 'c2', 'again', 'ch', 'pi', 'tn', 'nobody', 'beforehand', 'pj', 'th', 'fr', "we've", 'xt', 'first', 'ke', 'la', '6o', 'rs', 'fn', 'others', 'itself', "i've", 'world', 'entirely', 'instead', 'specifying', 'auth', 'ic', 'lj', 'p3', 'thereby', 'wheres', 'primarily', 'enough', 'ig', 'bd', 'gotten', 'isn', 'eighty', 'thin', 'much', 'example', 'available', '0s', 'under', 'forth', 'hj', "isn't", 'ge', 'ef', 'ord', 'please', 'secondly', 'himself', 'past', 'want', 'well', 'en', 'inner', 'thickv', 'at', 'pe', 'among', "hadn't", 'specifically', 'a1', 'affecting', "you'll", "that's", 'cg', 'iv', 'pu', 'ran', 'bill', 'take', 'four', 'should', 'bc', 'nr', 'fify', 'gs', 'uo', 'indicates', 'saying', 'py', 'beyond', 'known', 'if', 'wed', 'shall', 'really', 'although', 'be', 'whether', "that'll", "weren't", 'oj', 'looking', 'never', 'thousand', 'ah', 'need', 'rt', 'full', 'approximately', 'ignored', 'immediately', "mightn't", 'rm', 'some', 'taking', "who's", 'wi', 'your', 'through', 'd', "she'd", "she's", 'dp', 'xk', 'means', 'become', 'nine', 'between', 'twice', 'almost', 'invention', 'knows', 't1', 'go', 'specify', 'x1', 'arent', 'yours', 'thereafter', 'therere', 'asking', 'bp', 'despite', 'oo', 'perhaps', 'together', 'tp', 'herein', 'im', 'se', 'sf', 'most', 'both', "shan't", 'af', 'pas', 'r', 'an', 'ba'}

def clean_word(word):
    """Clean and normalize a word by removing punctuation and converting to lowercase."""
    # Remove all non-alphabetic characters
    cleaned = re.sub(r'[^a-zA-Z]', '', word)
    return cleaned.lower()

def extract_keywords(text):
    """Extract meaningful keywords from text by removing stopwords."""
    words = text.split()
    cleaned_words = []
    
    for word in words:
        cleaned = clean_word(word)
        if cleaned and len(cleaned) > 2 and cleaned not in stopwords:
            cleaned_words.append(cleaned)
    
    return list(set(cleaned_words))  # Return unique words

def calculate_score(resume_keywords, job_keywords):
    """Calculate match score based on keyword overlap."""
    if not job_keywords:
        return 0
    
    matched = set(resume_keywords) & set(job_keywords)
    score = (len(matched) / len(job_keywords)) * 100
    return min(score, 100)  # Cap at 100%

def extract_text_from_pdf(file_content):
    """Extract text from PDF content."""
    try:
        # Create a temporary file for PDF processing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(file_content)
            temp_file.flush()
            
            reader = PdfReader(temp_file.name)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        # Check if file was uploaded
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Please upload a PDF file only'}), 400
        
        # Get form data
        company_name = request.form.get('company_name', '').strip()
        job_description = request.form.get('job_description', '').strip()
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Extract text from PDF
        file_content = file.read()
        resume_text = extract_text_from_pdf(file_content)
        
        if not resume_text or len(resume_text.strip()) < 50:
            return jsonify({'error': 'Could not extract sufficient text from PDF. Please ensure the PDF contains readable text and is not password-protected.'}), 400
        
        # Extract keywords
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_description)
        
        # Calculate score and find matches
        score = calculate_score(resume_keywords, job_keywords)
        matched_keywords = list(set(resume_keywords) & set(job_keywords))
        suggested_keywords = list(set(job_keywords) - set(resume_keywords))
        
        # Limit suggestions to top 20 most relevant
        suggested_keywords = suggested_keywords[:20]
        
        # Create response
        response_data = {
            'score': round(score, 1),
            'matched_keywords': sorted(matched_keywords),
            'suggestions': sorted(suggested_keywords),
            'resume_preview': resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
            'matched_count': len(matched_keywords),
            'total_job_keywords': len(job_keywords),
            'total_resume_keywords': len(resume_keywords),
            'company_name': company_name
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Vercel expects a handler function
def handler(request):
    return app(request.environ, lambda status, headers: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True)
