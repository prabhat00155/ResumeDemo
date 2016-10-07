
function highlight(featureImportance) {

  const htmlToSearch = {
    companies: Array.from(document.querySelectorAll('.position .item-subtitle')).map(a=>a.firstChild),
    headline: Array.from(document.getElementsByClassName('headline title')),
    connections: Array.from(document.getElementsByClassName('member-connections')), // Note: has a strong tag
    skills: Array.from(document.getElementsByClassName('skill')).map(a=>a.getElementsByTagName('span')[0]),
    summary: Array.from(document.querySelectorAll('#summary .description p')),
    roles: Array.from(document.querySelectorAll('.position h4.item-title')),
    schools: Array.from(document.querySelectorAll('.schools .item-title')),
  };

  const ngramsToSkip = { '':true, '-':true, '_':true, ',':true, '.':true, '?:':true, 'undefined':true, };

  Object.keys(featureImportance).forEach(section => {
    const ngramRegexsPositives = [];
    const ngramRegexsNegatives = [];
    Object.keys(featureImportance[section]).forEach(ngram => {

      if (ngramsToSkip[ngram]) {
        console.warn(`Skipping n-gram: ${ngram}`)
      } else {
        const importance = featureImportance[section][ngram];
        const ngramSearchRegexText = ngram.replace(/[.?*+^$[\]\\(){}|-]/g, "\\$&").split('_').join('\\s');
        if (importance >= 0) { ngramRegexsPositives.push(ngramSearchRegexText); }
        else { ngramRegexsNegatives.push(ngramSearchRegexText); }
        console.log(`ngram=${ngram}`);
      }
    });

    // Create regex to search & replace on, sorted by longest first.
    ngramRegexsPositives.sort((a, b) => b.length - a.length);
    ngramRegexsNegatives.sort((a, b) => b.length - a.length);
    const ngramsSearchRegexPositives = new RegExp(ngramRegexsPositives.join('|'), 'gi');
    const ngramsSearchRegexNegatives = new RegExp(ngramRegexsNegatives.join('|'), 'gi');

    if (htmlToSearch[section]) {
      console.log(`ngramsSearchRegexPositives=${ngramsSearchRegexPositives}`);
      console.log(`ngramsSearchRegexNegatives=${ngramsSearchRegexNegatives}`);
      htmlToSearch[section].forEach(dom => {
        if (ngramRegexsPositives.length && (dom.innerHTML||'').match(ngramsSearchRegexPositives)) { dom.innerHTML = dom.innerHTML.replace(ngramsSearchRegexPositives, a=>`<span style='background-color:rgba(255, 0, 0, 0.7)'>${a}</span>`); }
        if (ngramRegexsNegatives.length && (dom.innerHTML||'').match(ngramsSearchRegexNegatives)) { dom.innerHTML = dom.innerHTML.replace(ngramsSearchRegexNegatives, a=>`<span style='background-color:rgba(0, 255, 20, 0.7);'>${a}</span>`); }
      });
    } else {
      console.error(`Please extract section: ${section}`);
    }
  });

  document.body.style.overflow='visible';
}

//var featureImportance = {"0 (accepted)":{"undefined":null},"roles":{"program manager":1, "data":-1,"engineer":-0.3771569,"analyst":-0.2214854,"analytics":-0.2155646,"scientist":-0.1922189,"-":0.0640342,"president":0.05838439,"director":0.09142493},"headline":{"data":-0.6861926,",":0.07813177},"skills":{"data":-0.2632319,"_":0.5742549},"companies":{"_":-0.7256273},"schools":{"_":-0.4342133},"summary":{"data":-0.2409923,"":0.1275924,",":0.2316926},"connections":{"500+":0.3418371}};
highlight(featureImportance);
