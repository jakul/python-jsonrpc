
"""
  Copyright (c) 2007 Jan-Klaas Kollhof

  This file is part of jsonrpc.

  jsonrpc is free software; you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation; either version 2.1 of the License, or
  (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this software; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import urllib2
from jsonrpc.json import dumps, loads, JSONDecodeException

class JSONRPCException(Exception):
    def __init__(self, rpcError):
        Exception.__init__(self)
        self.error = rpcError

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.error))
        
class ServiceProxy(object):
    def __init__(self, serviceURL, serviceName=None):
        self.__serviceURL = serviceURL
        self.__serviceName = serviceName

    def __getattr__(self, name):
        if self.__serviceName != None:
            name = "%s.%s" % (self.__serviceName, name)
        return ServiceProxy(self.__serviceURL, name)

    def __call__(self, *args):
         postdata = dumps({'method': self.__serviceName, 
                           'params': args, 
                           'id':'jsonrpc'})
         request = urllib2.Request(self.__serviceURL, postdata,
                                   {'Content-type': 'application/json'})
         respdata = urllib2.urlopen(request).read()
         try:
             resp = loads(respdata)
             if resp.get('error'):
                 raise JSONRPCException(resp['error'])
             else:
                 return resp['result']
         except JSONDecodeException:
             raise JSONDecodeException(respdata)
         

