#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

import mako
from .imagebackgroundsearch_rest import ImageBackgroundSearch
from .imagecontentsearch_rest import ImageContentSearch
from .imagedomaindynamicssearch_rest import ImageDomainDynamicsSearch
from .imagefeatures_rest import ImageFeatures
from .imagepivot_rest import ImagePivot
from .imagesearch_rest import ImageSearch
from .imageprefix_rest import ImagePrefix


class CustomAppRoot(object):
    """
    This serves the main index HTML file of the custom app from /
    """
    exposed = True

    indexHtml = None

    vars = {
        'apiRoot': 'api/v1',
        'staticRoot': 'static',
        'title': 'Image Space'
    }

    template = r"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <title>${title}</title>
        <link rel="stylesheet"
              href="${staticRoot}/lib/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet"
              href="${staticRoot}/lib/fontello/css/fontello.css">
        <link rel="stylesheet"
              href="${staticRoot}/lib/fontello/css/animation.css">
        <link rel="stylesheet"
              href="${staticRoot}/built/app.min.css">
        <link rel="stylesheet"
              href="${staticRoot}/built/plugins/imagespace/imagespace.min.css">
        <link rel="icon"
              type="image/png"
              href="${staticRoot}/img/Girder_Favicon.png">

        <style id="blur-style">
            img.im-blur {
                -webkit-filter: blur(10px);
                filter: blur(10px)
            }
        </style>

      </head>
      <body>
        <div id="g-global-info-apiroot" class="hide">${apiRoot}</div>
        <div id="g-global-info-staticroot" class="hide">${staticRoot}</div>

        <script>
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
            })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

            ga('create', 'UA-66442136-1', 'auto');
            ga('send', 'pageview');
        </script>

        <script src="${staticRoot}/built/libs.min.js"></script>
        <script src="${staticRoot}/built/app.min.js"></script>
        <script src="${staticRoot}/built/plugins/gravatar/plugin.min.js">
        </script>
        <script src="${staticRoot}/built/plugins/imagespace/imagespace-libs.min.js">
        </script>
        <script src="${staticRoot}/built/plugins/imagespace/imagespace.min.js">
        </script>
        <script src="${staticRoot}/built/plugins/imagespace/main.min.js"></script>
      </body>
    </html>
    """

    def GET(self):
        if self.indexHtml is None:
            self.indexHtml = mako.template.Template(self.template).render(
                **self.vars)

        return self.indexHtml


def load(info):
    # Bind our REST resources
    info['apiRoot'].imagebackgroundsearch = ImageBackgroundSearch()
    info['apiRoot'].imagecontentsearch = ImageContentSearch()
    info['apiRoot'].imagedomaindynamicssearch = ImageDomainDynamicsSearch()
    info['apiRoot'].imagesearch = ImageSearch()
    info['apiRoot'].imagefeatures = ImageFeatures()
    info['apiRoot'].imagepivot = ImagePivot()
    info['apiRoot'].imageprefix = ImagePrefix()

    # Move girder app to /girder, serve our custom app from /
    info['serverRoot'], info['serverRoot'].girder = (CustomAppRoot(),
                                                     info['serverRoot'])
    info['serverRoot'].api = info['serverRoot'].girder.api
