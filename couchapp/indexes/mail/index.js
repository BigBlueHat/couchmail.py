/**
Copyright 2014 Cloudant, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
**/

function (doc) {
  if ('to' in doc && 'from' in doc && 'subject' in doc && 'message' in doc) {
    index('default', [doc.subject, doc.message].join(' '));
    index('to', doc.to, {store: true, facet: true});
    index('from', doc.from, {store: true, facet: true});
    index('subject', doc.subject.replace('Re: ', '').replace('Fwd: ', ''),
      {store: true, facet: true});
    // generate a number based on year + month for range counting
    index('date', (doc.date[0]*100)+doc.date[1], {store: true, facet: true});
    index('full_date', doc.date[0]+'-'+doc.date[1]+'-'+doc.date[2]+'T'
        +doc.date[3]+':'+doc.date[4]+':'+doc.date[5], {store:true});
  }
}
