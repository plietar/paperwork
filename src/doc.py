import codecs
import os
import os.path
import time

class ScannedDoc(object):
    EXT_TXT = "txt"
    EXT_IMG = "jpg"

    def __init__(self, docpath, docid = None):
        """
        Arguments:
            docpath --- For an existing document, the path to its folder. For a new one, the rootdir of all documents
            docid --- Document Id (ie folder name). Use None for a new document
        """
        if docid == None:
            self.docid = time.strftime("%Y%m%d_%H%M_%S")
            self.docpath = os.path.join(docpath, self.docid)
        else:
            self.docid = docid
            self.docpath = docpath

    def get_nb_pages(self):
        # XXX(Jflesch): We try to not make assumptions regarding file names,
        # except regarding their extensions (.txt/.jpg/etc)
        try:
            filelist = os.listdir(self.docpath)
            i = 0
            for f in filelist:
                if f[-4:].lower() != "."+self.EXT_IMG:
                    continue
                i += 1
            return i
        except Exception, e:
            print "Exception while trying to get the number of pages of '%s': %s" % (self.docid, e)
            return 0

    def _get_filepath(self, page, ext):
        assert(page > 0)

        # XXX(Jflesch): We try to not make assumptions regarding file names,
        # except regarding their extensions (.txt/.jpg/etc)

        filelist = os.listdir(self.docpath)
        filelist.sort()
        i = 1
        for f in filelist:
            if f[-4:].lower() != "."+ext:
                continue
            if page == i:
                return os.path.join(self.docpath, f)
            i += 1
        raise Exception("Page %d not found in document '%s' !" % (page, self.docid))

    def get_txt_path(self, page):
        return self._get_filepath(page, self.EXT_TXT)

    def get_img_path(self, page):
        return self._get_filepath(page, self.EXT_IMG)

    def get_text(self, page):
        txtfile = self.get_txt_path(page)
        txt = ""
        with codecs.open(txtfile, encoding='utf-8') as fd:
            for line in fd.readlines():
                txt += line
        return txt

    def __str__(self):
        return self.docid