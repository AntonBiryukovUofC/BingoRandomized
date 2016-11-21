import numpy as np
import matplotlib.pyplot as plt
# Text Wrapping
# Defines wrapText which will attach an event to a given mpl.text object,
# wrapping it within the parent axes object.  Also defines a the convenience
# function textBox() which effectively converts an axes to a text box.
def wrapText(text, margin=7):
    """ Attaches an on-draw event to a given mpl.text object which will
        automatically wrap its string wthin the parent axes object.

        The margin argument controls the gap between the text and axes frame
        in points.
    """
    ax = text.get_axes()
    margin = margin / 72 * ax.figure.get_dpi()

    def _wrap(event):
        """Wraps text within its parent axes."""
        def _width(s):
            """Gets the length of a string in pixels."""
            text.set_text(s)
            return text.get_window_extent().width

        # Find available space
        clip = ax.get_window_extent()
        x0, y0 = text.get_transform().transform(text.get_position())
        if text.get_horizontalalignment() == 'left':
            width = clip.x1 - x0 - margin
        elif text.get_horizontalalignment() == 'right':
            width = x0 - clip.x0 - margin
        else:
            width = (min(clip.x1 - x0, x0 - clip.x0) - margin) * 2

        # Wrap the text string
        words = [''] + _splitText(text.get_text())[::-1]
        wrapped = []

        line = words.pop()
        while words:
            line = line if line else words.pop()
            lastLine = line

            while _width(line) <= width:
                if words:
                    lastLine = line
                    line += words.pop()
                    # Add in any whitespace since it will not affect redraw width
                    while words and (words[-1].strip() == ''):
                        line += words.pop()
                else:
                    lastLine = line
                    break

            wrapped.append(lastLine)
            line = line[len(lastLine):]
            if not words and line:
                wrapped.append(line)

        text.set_text('\n'.join(wrapped))

        # Draw wrapped string after disabling events to prevent recursion
        handles = ax.figure.canvas.callbacks.callbacks[event.name]
        ax.figure.canvas.callbacks.callbacks[event.name] = {}
        ax.figure.canvas.draw()
        ax.figure.canvas.callbacks.callbacks[event.name] = handles

    ax.figure.canvas.mpl_connect('draw_event', _wrap)

def _splitText(text):
    """ Splits a string into its underlying chucks for wordwrapping.  This
        mostly relies on the textwrap library but has some additional logic to
        avoid splitting latex/mathtext segments.
    """
    import textwrap
    import re
    math_re = re.compile(r'(?<!\\)\$')
    textWrapper = textwrap.TextWrapper()

    if len(math_re.findall(text)) <= 1:
        return textWrapper._split(text)
    else:
        chunks = []
        for n, segment in enumerate(math_re.split(text)):
            if segment and (n % 2):
                # Mathtext
                chunks.append('${}$'.format(segment))
            else:
                chunks += textWrapper._split(segment)
        return chunks

def textBox(text, axes, ha='left', fontsize=12, margin=None, frame=True, **kwargs):
    """ Converts an axes to a text box by removing its ticks and creating a
        wrapped annotation.
    """
    if margin is None:
        margin = 6 if frame else 0
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_frame_on(frame)

    an = axes.annotate(text, fontsize=fontsize, xy=({'left':0, 'right':1, 'center':0.5}[ha], 1), ha=ha, va='top',
                       xytext=(margin, -margin), xycoords='axes fraction', textcoords='offset points', **kwargs)
    wrapText(an, margin=margin)
    return an







with open('ProfessionalBank') as f:
    professional = f.readlines()
    
with open('InformalBank') as f:
    informal = f.readlines()



w,h=14,8.5
nr=5
nc=5
fig,ax = plt.subplots(ncols=nc,nrows=nr,figsize =(w,h))
nprof = 10
ninf=15

prof_subsample =np.random.choice(professional,size=nprof,replace=False)
inf_subsample =np.random.choice(informal,size=ninf,replace=False)
axIndices = np.random.permutation(range(nr*nc))
bingo_items = np.hstack((inf_subsample,prof_subsample))
np.random.shuffle(bingo_items)
for ind in axIndices:
    axInd=ax.flatten()[ind]
    #axInd.text(0,0,bingo_items[ind],wrap=True)
    if not(ind==12):
        an = axInd.annotate(bingo_items[ind], fontsize=14, xy=(0.5, 0.7), ha='center', va='top', xytext=(0, -6),
                 xycoords='axes fraction', textcoords='offset points')
    else:
        an = axInd.annotate('FREE', fontsize=18, xy=(0.5, 0.7), ha='center', va='top', xytext=(0, -6),
                 xycoords='axes fraction', textcoords='offset points')
            
    wrapText(an)
   # axInd.annotate(bingo_items[ind], xy=(0.1, 0.2), xycoords='axes fraction',wrap=True)
   
    axInd.set_xticks([])
    axInd.set_yticks([])
    axInd.set_yticklabels([])
    axInd.set_xticklabels([])
plt.tight_layout()
fig.subplots_adjust(top=0.9)
fig.suptitle('Icebreaker BINGO', fontsize=28)
fig.savefig('example.png',bbox_inches_tight=True)