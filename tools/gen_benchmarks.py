#!/usr/bin/env python3
"""
Programmatic generator for the /pmf-benchmark/[industry] page set + hub.

Run:
    python3 tools/gen_benchmarks.py

What it does (idempotent — safe to re-run):
  - Writes one HTML page per entry in INDUSTRIES to pmf-benchmark/<slug>.html
  - Rebuilds the hub at pmf-benchmark/index.html from HUBCARDS
  - Appends any missing benchmark URLs to sitemap.xml

To ADD a new industry (e.g. healthtech):
  1. Append a dict to INDUSTRIES (slug, name, kicker, title, desc, og, h1, dek,
     tldr[], body, faq[(q,a)], related[(href,text)]). Keep the body honest:
     the benchmark is always 40% — differentiate on HOW to measure in that vertical.
  2. Append a (slug, Name, blurb) tuple to HUBCARDS so the hub lists it.
  3. Re-run this script. The page, hub, and sitemap update automatically.
  The site-wide footer already links the hub (/pmf-benchmark), so individual
  industry pages need no footer change.

Honesty rule: never invent a per-industry PMF *number*. 40% is the cross-industry
Sean Ellis benchmark; the value of each page is vertical-specific measurement guidance.
"""
import os, re, json, html as H

# Repo root = parent of this tools/ directory (portable; no hardcoded path).
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://www.pmftracker.com"

NAV = '''<!-- ===== NAV ===== -->
<div data-animation="default" class="navbar_component w-nav" data-easing2="ease" data-easing="ease" data-collapse="medium" role="banner" data-duration="400"><div class="navbar_container"><a href="/" class="navbar_logo-link w-nav-brand"><img src="/images/link-20-e2-86-92-20pmf-20tracker.avif" loading="lazy" alt="Logo of PMF Tracker SaaS Firm" class="navbar-logo"/></a><nav role="navigation" class="navbar_menu is-page-height-tablet w-nav-menu"><a href="/#work" class="navbar-link w-nav-link">How it works?</a><a href="/#solution" class="navbar-link w-nav-link">Solution</a><a href="/#pricing" class="navbar-link w-nav-link">Pricing</a><a href="/for-vc" class="navbar-link w-nav-link">For VC</a><a href="/for-accelerators" class="navbar-link w-nav-link">For Accelerators</a><div class="pmf-navdrop"><a tabindex="0" class="navbar-link w-nav-link pmf-navdrop-toggle">Tools</a><div class="pmf-navdrop-menu"><a href="/pmf-score">PMF Score Calculator</a><a href="/sean-ellis-survey">Sean Ellis Survey Template</a><a href="/pmf-investor-report">Investor PMF Report</a><a href="/pmf-benchmark">PMF Benchmarks by Industry</a></div></div><a href="/blog" class="navbar-link w-nav-link">Blog</a><a href="https://app.pmftracker.com/" class="button is-icon button-gray hide-desktop w-inline-block"><div class="button-text-purple">Get started</div></a></nav><div class="navbar_button-wrap"><a href="https://app.pmftracker.com/" class="button is-icon button-gray hide-tablet w-inline-block"><div class="button-text-purple">Get started</div><div class="icon-1x1-small purple-icon w-embed"><svg xmlns="http://www.w3.org/2000/svg" width="21" height="20" viewBox="0 0 21 20" fill="none"><path d="M3.86336 10H17.1967M17.1967 10L12.1967 5M17.1967 10L12.1967 15" stroke="#4D455E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div></a><div class="navbar_menu-button w-nav-button"><div class="rl_menu-icon2"><div class="rl_menu-icon2_line-top"></div><div class="rl_menu-icon2_line-middle"><div class="rl_menu-icon_line-middle-inner"></div></div><div class="rl_menu-icon2_line-bottom"></div></div></div></div></div></div>'''

FOOTER = '''<!-- ===== FOOTER ===== -->
<div class="footer_component overflow-hidden"><div class="padding-global is-footer"><div class="container-large"><div class="w-layout-grid footer_top-wrapper"><a href="/" class="footer_logo-link w-nav-brand"><img src="/images/links.avif" loading="lazy" alt="PMF Brand Mark - Go back to the home page" class="footer_logo"/></a><div class="w-layout-grid footer_link-list"><div class="footer_mail_wrap"><div class="footer_header_wrap"><p class="heading-style-h6">Get in Touch</p><p class="footer-text">We&#x27;re here to help. You can reach us <br/>via email or our social media.</p></div><div class="footer_mail"><img src="/images/ic_sharp-mail.webp" loading="lazy" alt="" class="mail"/><a href="mailto:hello@pmftracker.com?subject=Hi%20there" class="footer-mail-text">hello@pmftracker.com</a></div><div class="pmf-foot-connect"><p class="pmf-foot-h is-sub">Connect</p><a href="https://www.linkedin.com/company/pmftracker" target="_blank" class="footer-link">LinkedIn</a><a href="mailto:hello@pmftracker.com?subject=Hi%20there" class="footer-link">Email us</a></div></div><div class="pmf-foot-col"><p class="pmf-foot-h">Product</p><a href="/#work" class="footer-link">How it works?</a><a href="/#solution" class="footer-link">Solution</a><a href="/#pricing" class="footer-link">Pricing</a><a href="/for-vc" class="footer-link">For VCs</a><a href="/for-accelerators" class="footer-link">For Accelerators</a><a href="/#faq" class="footer-link">FAQ</a><a href="https://app.pmftracker.com/" class="footer-link">Start Free</a><a href="https://cal.com/pmftracker/product-demo" class="footer-link">Book Demo</a></div><div class="pmf-foot-col"><p class="pmf-foot-h">Tools</p><a href="/pmf-score" class="footer-link">PMF Score Calculator</a><a href="/sean-ellis-survey" class="footer-link">Sean Ellis Survey Template</a><a href="/pmf-investor-report" class="footer-link">Investor PMF Report</a><a href="/pmf-benchmark" class="footer-link">PMF Benchmarks by Industry</a><p class="pmf-foot-h is-sub">Compare</p><a href="/vs/pmfsurvey" class="footer-link">vs PMFsurvey.com</a><a href="/vs/typeform-spreadsheet" class="footer-link">vs Typeform + Sheets</a><a href="/vs/survicate" class="footer-link">vs Survicate</a><a href="/vs/tally" class="footer-link">vs Tally</a><a href="/vs/surveymonkey" class="footer-link">vs SurveyMonkey</a></div><div class="pmf-foot-col"><p class="pmf-foot-h">Articles</p><a href="/blog" class="footer-link">All articles</a><a href="/blog/sean-ellis-40-percent-rule" class="footer-link">The Sean Ellis 40% Rule</a><a href="/blog/superhuman-pmf-engine" class="footer-link">Superhuman: 22% &#8594; 58%</a><a href="/blog/how-to-measure-product-market-fit" class="footer-link">How to Measure PMF</a><a href="/blog/how-to-improve-pmf-score" class="footer-link">Improve Your PMF Score</a></div></div></div><div class="divider_container"><div class="footer_line-divider"></div></div><div class="w-layout-grid footer_bottom-wrap"><div class="footer_settings_wrap"><a href="/terms-and-conditions" class="rl_footer4_legal-link">Terms and Conditions</a><a href="/privacy-policy" class="rl_footer4_legal-link">Privacy Policy</a><a href="/privacy-policy" class="rl_footer4_legal-link">Cookies Settings</a></div><div class="footer_credit-text">© 2025 PMFtracker. All rights reserved.</div></div></div></div></div>'''

GTM_HEAD = '''<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-KS6486GZ');</script>
<!-- End Google Tag Manager -->'''

GTM_BODY = '''<script src="/js/jquery.js" type="text/javascript"></script>
<script src="/js/webflow.schunk.36b8fb49256177c8.js" type="text/javascript"></script>
<script src="/js/webflow.schunk.9d5021b1f222040f.js" type="text/javascript"></script>
<script src="/js/webflow-script.js" type="text/javascript"></script>
<script src="/js/lead.js" defer></script>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KS6486GZ"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->'''

BYLINE = '''    <div class="article-byline">
      <div class="article-byline-avatar"><img src="/images/au_profile_photo_2025-20copy-201-p-500.webp" width="44" height="44" alt="Olek Uznanski" loading="lazy"/></div>
      <div class="article-byline-text">
        <strong>Olek Uznanski · Founder, PMFtracker</strong>
        <span>Product leader who's trained 200+ startups on product-market fit</span>
      </div>
    </div>'''

CTA_MID = '''    <div class="cta-box">
      <h3>See where you land against 40%</h3>
      <p>The free PMF score calculator runs the Sean Ellis survey on your users and shows your score against the benchmark — no signup.</p>
      <a href="/pmf-score" class="cta-btn">Calculate your PMF score →</a>
      <span class="cta-sub">Built on the Sean Ellis 40% method.</span>
    </div>'''

def jld(obj): return '<script type="application/ld+json">'+json.dumps(obj,separators=(',',':'),ensure_ascii=False)+'</script>'

def esc_attr(s): return s.replace('&','&amp;').replace('"','&quot;')

def render_article(slug, title, desc, og_desc, kicker, h1, dek, tldr_items, body_html,
                   faq, related, breadcrumb_name, parent=None):
    url = f"{B}/pmf-benchmark/{slug}" if slug else f"{B}/pmf-benchmark"
    # schema
    article = {"@context":"https://schema.org","@type":"Article","headline":title.split(" | ")[0],
        "description":desc,"author":{"@type":"Person","name":"Olek Uznanski","jobTitle":"Founder, PMFtracker",
        "image":B+"/images/au_profile_photo_2025-20copy-201.webp","description":"Product leader who has trained 200+ startups on product-market fit."},
        "publisher":{"@type":"Organization","name":"PMFtracker","logo":{"@type":"ImageObject","url":B+"/images/links.avif"}},
        "mainEntityOfPage":url,"datePublished":"2026-06-21T09:00:00+00:00","dateModified":"2026-06-21T09:00:00+00:00",
        "image":B+"/images/og-image.avif"}
    faqpage = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    crumbs=[{"@type":"ListItem","position":1,"name":"Home","item":B+"/"}]
    pos=2
    crumbs.append({"@type":"ListItem","position":pos,"name":"PMF Benchmarks","item":B+"/pmf-benchmark"}); pos+=1
    if slug:
        crumbs.append({"@type":"ListItem","position":pos,"name":breadcrumb_name,"item":url})
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":crumbs}

    tldr = "\n        ".join(f"<li>{x}</li>" for x in tldr_items)
    faq_html = "\n    ".join(
        f'<div class="faq-item">\n      <h3>{q}</h3>\n      <p>{a}</p>\n    </div>' for q,a in faq)
    rel_html = "\n      ".join(f'<li><a href="{href}">{txt} →</a></li>' for href,txt in related)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>{title}</title>
<link href="{url}" rel="canonical"/>
<meta name="description" content="{esc_attr(desc)}"/>
<meta content="{esc_attr(title.split(" | ")[0])}" property="og:title"/>
<meta content="{esc_attr(og_desc)}" property="og:description"/>
<meta content="{url}" property="og:url"/>
<meta content="https://www.pmftracker.com/images/og-image.avif" property="og:image"/>
<meta property="og:type" content="article"/>
<meta content="summary_large_image" name="twitter:card"/>
<link href="/css/pmftrackerr.webflow.shared.53ff0c310.css" rel="stylesheet" type="text/css"/>
<link href="/css/blog.css" rel="stylesheet" type="text/css"/>
<link href="/images/favicon.png" rel="shortcut icon" type="image/x-icon"/><link href="/images/app-icon.png" rel="apple-touch-icon"/>
{jld(article)}
{jld(faqpage)}
<link href="/css/site.css" rel="stylesheet" type="text/css"/>

{GTM_HEAD}
<!-- pmf-breadcrumb -->{jld(bc)}</head>
<body class="body blog-page">

{NAV}

<main class="blog-shell">

  <header class="article-head">
    <a href="/pmf-benchmark" class="blog-back">← PMF benchmarks by industry</a>
    <div class="article-kicker">{kicker}</div>
    <h1>{h1}</h1>
    <p class="article-dek">{dek}</p>
{BYLINE}
  </header>

  <div class="blog-wrap">
    <div class="tldr">
      <h2>TL;DR</h2>
      <ul>
        {tldr}
      </ul>
    </div>
  </div>

  <article class="article-body">

{body_html}

  </article>


  <!-- ===== FAQ ===== -->
  <section class="faq-section">
    <h2>Frequently asked questions</h2>
    {faq_html}
  </section>

  <!-- ===== LEAD MAGNET ===== -->
  <div class="lp-calc-wrap">
    <div class="cta-box lead-cta">
      <h3>Get the PMF Benchmark Kit</h3>
      <p>We'll email you the full kit — the Sean Ellis survey template, scoring sheet, and the how-to-measure guide for your vertical.</p>
      <button type="button" class="cta-btn" data-lead-open="magnet" data-lead-asset="the PMF Benchmark Kit">Email me the kit →</button>
      <span class="cta-sub">Straight to your inbox · No spam, unsubscribe anytime.</span>
    </div>
  </div>

  <!-- ===== RELATED ===== -->
  <nav class="related">
    <h2>Keep reading</h2>
    <ul class="related-list">
      {rel_html}
    </ul>
  </nav>

</main>

{FOOTER}

{GTM_BODY}
</body>
</html>
'''

# ---------------- INDUSTRY CONTENT (hand-authored, differentiated) ----------------
CTA_END = '''    <div class="cta-box">
      <h3>Measure your fit, find your ICP, track the trend</h3>
      <p>PMFtracker runs the Sean Ellis survey on your engaged users, scores you against the 40% benchmark, surfaces your ICP from the open-ended answers, and tracks the trend over time.</p>
      <a href="https://app.pmftracker.com/" class="cta-btn">Start measuring free →</a>
      <span class="cta-sub">Set up in 5 minutes · No credit card required</span>
    </div>'''

INDUSTRIES = []

def body(parts): return "\n\n".join(parts)

# ---- SaaS ----
INDUSTRIES.append(dict(
 slug="saas", name="SaaS", kicker="SaaS",
 title="PMF Benchmark for SaaS: What's a Good Score? | PMFtracker",
 desc="What's a good PMF score for a SaaS startup? The benchmark is 40% — here's how to measure product-market fit in SaaS, who to survey, and the trap to avoid.",
 og="The PMF benchmark for SaaS is 40%. Who counts as an engaged user, what 'very disappointed' looks like, and how Slack and Superhuman measured it.",
 h1="PMF benchmark for SaaS: what's a good product-market fit score?",
 dek="If you're building a SaaS product and wondering what PMF score to aim for, the answer is the same one Slack and Superhuman used: 40%. What's specific to SaaS isn't the number — it's who you survey and how you read the result.",
 tldr=[
  "The PMF benchmark for SaaS is <strong>40%</strong> on the Sean Ellis test — the same cross-industry line, not a SaaS-specific number.",
  "Survey <strong>activated users</strong> who've completed onboarding and used the core workflow recently — not free-trial tourists or the buyer who never logs in.",
  "Reference points: <strong>Slack 51%</strong>, <strong>Superhuman 22% → 58%</strong>, both SaaS.",
  "The SaaS trap: a buyer-vs-user split. Survey the person who actually does the work in the product.",
 ],
 body=body([
  "<p>SaaS is the home turf of the PMF survey. The most-cited product-market fit stories — Slack, Superhuman, Dropbox — are all SaaS, and the Sean Ellis test was popularized measuring exactly this kind of product. So if you run a SaaS startup, you're in luck: the playbook is well-worn.</p>",
  "<p>The benchmark you're aiming for is <strong>40%</strong>: at least 40% of your engaged users saying they'd be \"very disappointed\" to lose the product.</p>",
  '<div class="callout"><p class="formula">Is the PMF benchmark different for SaaS? No — it\'s still 40%. What\'s different is who you ask and how you read it.</p></div>',
  "<h2>Who counts as an engaged user in SaaS</h2>",
  "<p>This is where most SaaS founders get a misleading score. Your signup list is full of people who created an account, poked around once, and vanished. Survey all of them and your number reads artificially low, because the tire-kickers were never going to care.</p>",
  "<p>An engaged SaaS user is someone who has <strong>completed onboarding and used your core workflow a handful of times in the last few weeks</strong> — an active seat, not a dormant one. Those are the people whose answer to \"how would you feel without this?\" actually means something.</p>",
  "<h2>The SaaS-specific trap: buyer vs user</h2>",
  "<p>In B2B SaaS, the person who <em>bought</em> the tool is often not the person who <em>uses</em> it. The admin who signed the contract may never touch the core feature. If you survey buyers, you measure purchasing satisfaction; if you survey users, you measure product-market fit. You want the second one.</p>",
  '<div class="pullquote">Survey the person who does the work in your product, not the person who approved the invoice.</div>',
  "<h2>What \"very disappointed\" looks like in SaaS</h2>",
  "<p>When Slack hit 51%, users said it made them more productive and improved how their team collaborated. Superhuman's fans were speed-obsessed power users. The pattern in SaaS is the same: the people who'd be devastated to lose you have <strong>woven the product into a daily workflow</strong>. Read the open-ended answers and you'll usually find a job-to-be-done your most disappointed users can't imagine doing any other way. That's your ICP.</p>",
  "<h2>How to measure PMF in SaaS</h2>",
  "<ul>"
  "<li><strong>Filter to active users.</strong> Define \"engaged\" (e.g. used the core feature 3+ times in 14 days) and survey only them.</li>"
  "<li><strong>Survey the user, not the buyer.</strong> In B2B, route the question to the person in the product daily.</li>"
  "<li><strong>Mine the open-ends.</strong> \"Very disappointed\" answers reveal your ICP and core value; \"somewhat\" answers reveal what's blocking conversion.</li>"
  "<li><strong>Track the trend.</strong> Superhuman went 22% → 58% by treating the score as a metric to move every cycle, not a one-time grade.</li>"
  "</ul>",
  "<p>SaaS gives you something most industries don't: clean usage data to define engagement, and a product people open every day. Use both. The score is only as honest as the users you point it at.</p>",
  CTA_END,
 ]),
 faq=[
  ("What's a good PMF score for a SaaS startup?","40% or more on the Sean Ellis test — the same cross-industry benchmark. At least 40% of your engaged users should say they'd be \"very disappointed\" to lose the product. Slack scored 51% and Superhuman reached 58%, both SaaS."),
  ("Who should I survey to measure SaaS product-market fit?","Activated users — people who've completed onboarding and used your core workflow a few times in the last couple of weeks. In B2B, survey the person who uses the product daily, not the buyer who approved it. Surveying dormant signups will understate your score."),
  ("Is product-market fit different for B2B vs B2C SaaS?","The 40% benchmark holds for both. The difference is the buyer-vs-user split in B2B (survey the user) and the smaller, higher-intent audience compared with consumer products. Define \"engaged\" appropriately for each and the test works the same way."),
 ],
 related=[("/blog/how-slack-measured-product-market-fit","How Slack measured product-market fit: the 51% survey"),
          ("/blog/superhuman-pmf-engine","How Superhuman went from 22% to 58% PMF score"),
          ("/blog/what-is-a-good-pmf-score","What's a good PMF score? The 40% benchmark"),
          ("/pmf-score","Try the free PMF score calculator")],
))

# ---- Fintech ----
INDUSTRIES.append(dict(
 slug="fintech", name="fintech", kicker="Fintech",
 title="PMF Benchmark for Fintech: What's a Good Score? | PMFtracker",
 desc="What's a good PMF score for a fintech startup? The benchmark is 40% — here's how to measure product-market fit in fintech, who to survey, and the trust factor.",
 og="The PMF benchmark for fintech is 40%. Why you survey funded, active accounts — and how Nubank uses the Sean Ellis score to guide product decisions.",
 h1="PMF benchmark for fintech: what's a good product-market fit score?",
 dek="Fintech adds something most products don't have to measure: trust with people's money. The PMF benchmark is still 40% — but who you survey, and how high the bar for \"very disappointed\" really is, are particular to financial products.",
 tldr=[
  "The PMF benchmark for fintech is <strong>40%</strong> — the standard Sean Ellis line, not a fintech-specific number.",
  "Survey <strong>funded, active accounts</strong> — people who've moved real money — not the signups who never cleared onboarding or KYC.",
  "<strong>Nubank</strong> has spoken about using the Sean Ellis score to guide decisions about new products.",
  "In fintech, \"very disappointed\" is a high bar — it usually means trust. That makes a strong score especially meaningful.",
 ],
 body=body([
  "<p>Fintech has a measurement quirk no other category shares quite so sharply: a huge share of your signups never become users at all. KYC checks, funding steps, and approval flows mean a long gap between \"created an account\" and \"actually uses this for money.\" Measure PMF across everyone and you'll drown the signal.</p>",
  "<p>The target is the usual one — <strong>40%</strong> \"very disappointed\" — but getting an honest read depends entirely on surveying the right accounts.</p>",
  '<div class="callout"><p class="formula">Is the PMF benchmark different for fintech? No — it\'s still 40%. What changes is that you only count accounts that have actually moved money.</p></div>',
  "<h2>Who counts as an engaged user in fintech</h2>",
  "<p>An engaged fintech user is a <strong>funded, active account</strong> — someone who has completed onboarding, passed KYC, and used the product for a real transaction. Signups stuck in the activation funnel aren't telling you about product-market fit; they're telling you about your onboarding. Keep those two questions separate.</p>",
  "<h2>The trust factor</h2>",
  "<p>In most products, \"very disappointed\" means a workflow gets harder. In fintech, it usually means something deeper: <strong>I trust this with my money and I don't want to move it.</strong> Switching a financial product is painful and a little scary, so a user who'd be genuinely disappointed to lose you has handed over real trust. That makes a strong fintech score especially load-bearing — and a weak one a warning that you're a convenience, not a home for someone's money.</p>",
  '<div class="pullquote">In fintech, "very disappointed" is rarely about features. It\'s about trust — and trust is the moat.</div>',
  "<h2>Nubank measured it</h2>",
  "<p>Nubank, one of the largest digital banks in the world, has talked about using the Sean Ellis \"very disappointed\" score as a key input when deciding whether to invest in new products. If a survey-based PMF score is good enough to steer product strategy at that scale, it's good enough for an early-stage fintech deciding what to build next.</p>",
  "<h2>How to measure PMF in fintech</h2>",
  "<ul>"
  "<li><strong>Survey funded, active accounts only.</strong> Exclude signups stuck in onboarding — they measure your funnel, not your fit.</li>"
  "<li><strong>Separate activation from fit.</strong> Low activation is an onboarding problem; a low score among active users is a product problem. Don't conflate them.</li>"
  "<li><strong>Read the \"why\" for trust signals.</strong> Open-ended answers about safety, control, and reliability are gold in fintech — they're your positioning.</li>"
  "<li><strong>Track it over time.</strong> Trust compounds. A rising score is the cleanest evidence your financial product is becoming a default, not a trial.</li>"
  "</ul>",
  "<p>The 40% line is the same. The discipline fintech demands is being ruthless about who you survey — because a financial product's signup list and its real user base are two very different things.</p>",
  CTA_END,
 ]),
 faq=[
  ("What's a good PMF score for a fintech startup?","40% or more on the Sean Ellis test, measured among funded, active accounts. In fintech a \"very disappointed\" answer usually signals trust, which makes a strong score especially meaningful. Nubank has used the same score to guide product decisions."),
  ("Who should I survey to measure fintech product-market fit?","Accounts that have completed onboarding and KYC and used the product for a real transaction. Signups stuck in the activation funnel tell you about onboarding, not product-market fit — survey them separately if at all."),
  ("Why is trust important when measuring PMF in fintech?","Because switching a financial product is painful and risky, a user who'd be \"very disappointed\" to lose you has handed over real trust, not just convenience. That makes the score a strong signal — and the open-ended answers about safety and control double as your positioning."),
 ],
 related=[("/blog/what-is-a-good-pmf-score","What's a good PMF score? The 40% benchmark"),
          ("/blog/sean-ellis-40-percent-rule","The Sean Ellis 40% rule, explained"),
          ("/blog/how-to-run-a-pmf-survey","How to run a PMF survey (with the exact questions)"),
          ("/pmf-score","Try the free PMF score calculator")],
))

# ---- Marketplace ----
INDUSTRIES.append(dict(
 slug="marketplace", name="marketplaces", kicker="Marketplaces",
 title="PMF Benchmark for Marketplaces: A Good Score | PMFtracker",
 desc="What's a good PMF score for a marketplace? The benchmark is 40% — but you measure it per side. How to run the Sean Ellis survey on supply and demand.",
 og="The PMF benchmark for marketplaces is 40% — measured per side. Why supply and demand need separate scores, and what Airbnb teaches.",
 h1="PMF benchmark for marketplaces: what's a good product-market fit score?",
 dek="Marketplaces are two products in a trench coat. The 40% benchmark still applies — but a single blended score hides more than it reveals, because supply and demand can have wildly different fit.",
 tldr=[
  "The PMF benchmark for marketplaces is <strong>40%</strong> — but you measure it <strong>per side</strong>, not as one blended number.",
  "An engaged user is someone who has <strong>completed a transaction recently</strong> — a buyer who bought, a seller who sold.",
  "<strong>Airbnb</strong> is the canonical example of manufacturing fit by fixing the constrained side (supply) by hand.",
  "A great score on one side and a weak one on the other still means no marketplace. Watch the weaker side.",
 ],
 body=body([
  "<p>A marketplace doesn't have one product-market fit. It has two — one for buyers, one for sellers — and they can be in completely different places. A blended 40% can hide a thriving demand side propped up against a supply side that's about to churn out. So the benchmark is the same; the unit of measurement is different.</p>",
  '<div class="callout"><p class="formula">Is the PMF benchmark different for marketplaces? No — it\'s still 40%. But you run the survey twice: once per side.</p></div>',
  "<h2>Who counts as an engaged user in a marketplace</h2>",
  "<p>On both sides, engagement means a <strong>completed transaction</strong>, recently. A buyer who browsed but never bought, or a seller who listed but never sold, hasn't experienced the marketplace's core promise — liquidity. Survey people who've actually transacted, and survey each side separately.</p>",
  "<h2>Measure the side you're constrained on</h2>",
  "<p>Most marketplaces are bottlenecked on one side — usually supply. That's the side whose PMF score you should watch most closely, because it's the one that will break first. A 60% score among buyers is worthless if sellers are at 20% and leaving. The constrained side <em>is</em> your growth ceiling.</p>",
  '<div class="pullquote">A marketplace is only as healthy as its weaker side. Score them separately, and watch the one that\'s about to churn.</div>',
  "<h2>What Airbnb did</h2>",
  "<p>Airbnb's early numbers were flat because the supply side wasn't working — listings had terrible photos and weren't converting. The founders didn't run a survey to learn this; they flew to New York and fixed it by hand, shooting professional photos themselves. Bookings climbed. The lesson translates directly: when one side of your marketplace is dragging, that's where your fit problem is, and that's the side to measure and obsess over.</p>",
  "<h2>How to measure PMF in a marketplace</h2>",
  "<ul>"
  "<li><strong>Run the survey twice.</strong> Once for buyers who bought, once for sellers who sold. Keep the scores separate.</li>"
  "<li><strong>Define engagement as a completed transaction.</strong> Browsing isn't experiencing the product; transacting is.</li>"
  "<li><strong>Prioritize the constrained side.</strong> Your overall fit is capped by whichever side scores lower.</li>"
  "<li><strong>Read the \"why\" for liquidity language.</strong> \"I can always find what I need\" (demand) and \"I get reliable buyers\" (supply) are the value props you want to hear.</li>"
  "</ul>",
  "<p>One marketplace, two scores. Blend them and you'll feel fine right up until the weaker side collapses. Measure them apart and you'll see the problem while there's still time to fix it.</p>",
  CTA_END,
 ]),
 faq=[
  ("What's a good PMF score for a marketplace?","40% or more on the Sean Ellis test — but measured per side. Run the survey separately for buyers and sellers, since the two sides can have very different product-market fit, and your overall health is capped by the weaker side."),
  ("How do I measure product-market fit for a two-sided marketplace?","Survey each side separately, counting only users who've completed a transaction recently. Pay closest attention to the side you're constrained on (usually supply) — a strong score on one side means nothing if the other is churning."),
  ("Who counts as an engaged marketplace user?","Someone who has completed a transaction: a buyer who bought or a seller who sold, recently. People who only browsed or listed haven't experienced the marketplace's core promise of liquidity, so their answers won't reflect real product-market fit."),
 ],
 related=[("/blog/product-market-fit-examples","Product-market fit examples: how 8 startups found it"),
          ("/blog/what-is-a-good-pmf-score","What's a good PMF score? The 40% benchmark"),
          ("/blog/how-to-know-if-you-have-product-market-fit","How to know if you have product-market fit: 6 signals"),
          ("/pmf-score","Try the free PMF score calculator")],
))

# ---- Consumer / B2C ----
INDUSTRIES.append(dict(
 slug="consumer-apps", name="consumer apps", kicker="Consumer / B2C",
 title="PMF Benchmark for Consumer Apps: A Good Score | PMFtracker",
 desc="What's a good PMF score for a consumer app? The benchmark is 40% — measured among habitual users. How to read PMF for B2C, with the Instagram example.",
 og="The PMF benchmark for consumer apps is 40%, measured among habitual users. Why B2C's huge top-of-funnel distorts the score, and what Instagram shows.",
 h1="PMF benchmark for consumer apps: what's a good product-market fit score?",
 dek="Consumer products live and die on habit. The 40% benchmark still applies — but B2C's enormous, casual top-of-funnel makes who you survey the difference between a true read and a flattering one.",
 tldr=[
  "The PMF benchmark for consumer apps is <strong>40%</strong> — the standard line, measured among <strong>habitual users</strong>.",
  "B2C has a huge casual top-of-funnel; survey people who use the app regularly (recent DAU/WAU), not every download.",
  "<strong>Instagram</strong> found fit by stripping a cluttered app down to the one habit that stuck — photo sharing.",
  "In consumer, the \"very disappointed\" core is smaller but mightier — it drives the word-of-mouth that powers B2C growth.",
 ],
 body=body([
  "<p>Consumer apps get a lot of tourists. Millions of downloads, a flood of curious one-time openers, and a much smaller core of people who actually formed a habit. That gap is the central challenge of measuring B2C product-market fit: if you survey everyone who ever installed the app, the casual majority will bury the signal from the people who genuinely love it.</p>",
  "<p>The benchmark is still <strong>40%</strong>. The art is pointing it at the right users.</p>",
  '<div class="callout"><p class="formula">Is the PMF benchmark different for consumer apps? No — it\'s still 40%. What\'s different is that you measure it among habitual users, not every download.</p></div>',
  "<h2>Who counts as an engaged user in B2C</h2>",
  "<p>An engaged consumer user is someone with a <strong>habit</strong> — they've used the app multiple times in the last week or two, not just on install day. Daily- and weekly-active users are your population. The one-time openers aren't a PMF signal; they're a retention or onboarding story, and a different problem to solve.</p>",
  "<h2>The small-but-mighty core</h2>",
  "<p>Here's the consumer twist: the group that would be \"very disappointed\" to lose your app is often a smaller slice of your total users than in B2B — but it punches far above its weight. That core is who posts about you, tells friends, and drives the organic, compounding growth that consumer products run on. A focused 45% among habitual users beats a mushy 25% across everyone every time.</p>",
  '<div class="pullquote">In consumer, your "very disappointed" users are your growth engine. They\'re the ones who tell everyone.</div>',
  "<h2>What Instagram did</h2>",
  "<p>Instagram started as Burbn, a cluttered app stuffed with check-ins, plans, and photos. Looking at actual usage, the founders saw one behavior carrying everything — photo sharing — and deleted the rest. The focused relaunch pulled in roughly 25,000 users on day one. The PMF lesson for consumer: don't average across a bloated product. Find the one habit your most engaged users can't live without, and measure <em>that</em>.</p>",
  "<h2>How to measure PMF in a consumer app</h2>",
  "<ul>"
  "<li><strong>Survey habitual users.</strong> Filter to recent daily/weekly actives. Casual installers will drag your score down and tell you nothing useful.</li>"
  "<li><strong>Expect a smaller, more intense core.</strong> Don't be discouraged by a modest total — a passionate 40%+ among regulars is real fit.</li>"
  "<li><strong>Read the \"why\" for the habit.</strong> The open-ends reveal the single behavior that makes people stay. Lean into it.</li>"
  "<li><strong>Track it as you ship.</strong> Consumer tastes move fast; a tracked score catches erosion before retention charts do.</li>"
  "</ul>",
  "<p>Consumer PMF isn't about pleasing the masses who tried you once. It's about how deeply your regulars would miss you — because they're the ones who'll bring the masses back.</p>",
  CTA_END,
 ]),
 faq=[
  ("What's a good PMF score for a consumer app?","40% or more on the Sean Ellis test, measured among habitual users (recent daily or weekly actives). In B2C the passionate core is smaller but drives word-of-mouth, so a focused 40%+ among regulars matters more than a blended score across all downloads."),
  ("Who should I survey to measure consumer product-market fit?","People who've formed a habit — used the app several times in the last week or two — not every download. One-time installers reflect onboarding and retention, not product-market fit, and surveying them will understate your true score."),
  ("Why is the engaged core smaller for consumer products?","Consumer apps attract a huge casual top-of-funnel of curious one-time users. The group that would be \"very disappointed\" to lose you is a smaller slice — but it's the slice that posts, refers, and drives the organic growth B2C depends on."),
 ],
 related=[("/blog/product-market-fit-examples","Product-market fit examples: how 8 startups found it"),
          ("/blog/what-product-market-fit-feels-like","What product-market fit actually feels like"),
          ("/blog/what-is-a-good-pmf-score","What's a good PMF score? The 40% benchmark"),
          ("/pmf-score","Try the free PMF score calculator")],
))

# ---- AI startups ----
INDUSTRIES.append(dict(
 slug="ai-startups", name="AI startups", kicker="AI",
 title="PMF Benchmark for AI Startups: A Good Score | PMFtracker",
 desc="What's a good PMF score for an AI startup? The benchmark is 40% — but novelty inflates early enthusiasm. How to measure real PMF for AI products.",
 og="The PMF benchmark for AI startups is 40%. Why demo-wow isn't fit, how novelty distorts the score, and who to survey for AI products.",
 h1="PMF benchmark for AI startups: what's a good product-market fit score?",
 dek="AI made building 10x cheaper but didn't make demand any easier to validate. The benchmark is still 40% — and for AI products, separating genuine fit from novelty is the whole game.",
 tldr=[
  "The PMF benchmark for AI startups is <strong>40%</strong> — the same Sean Ellis line, no AI exception.",
  "The AI trap is <strong>novelty</strong>: a jaw-dropping demo gets people to try once. Fit is whether they come back and rely on it.",
  "Survey <strong>repeat users</strong> who trust the output enough to use it for real work — not first-session wow.",
  "AI made building cheap, so \"no market need\" is a bigger risk than ever. Measuring fit is the antidote.",
 ],
 body=body([
  "<p>AI products have a measurement problem unique to the moment: the demo is so good it lies to you. A slick first impression gets thousands of people to sign up and try it once. Early enthusiasm spikes. And then a lot of them never come back — because \"wow, neat\" is not the same as \"I depend on this.\"</p>",
  "<p>The benchmark is the ordinary <strong>40%</strong>. The discipline AI demands is refusing to let novelty inflate it.</p>",
  '<div class="callout"><p class="formula">Is the PMF benchmark different for AI startups? No — it\'s still 40%. The hard part is making sure the score reflects retention, not novelty.</p></div>',
  "<h2>Why \"no market need\" is the AI-era risk</h2>",
  "<p>The biggest reason startups fail is building something nobody needs — and AI has made that easier, not harder. When you can ship a product in a weekend, the temptation is to skip validation entirely and let the technology be the pitch. But cheaper building doesn't create demand; it just means more products chasing the same unmet (or non-existent) needs. A PMF score is how you find out whether you're solving a real problem or just demoing a capability. <a href=\"/blog/no-market-need-ai-discovery\">More on why discovery matters more than ever.</a></p>",
  "<h2>Who counts as an engaged user for an AI product</h2>",
  "<p>An engaged AI user is someone who has <strong>come back and used the product for real work, repeatedly</strong>, and trusts the output enough to act on it. First-session users are reacting to novelty. Repeat users who've folded the tool into a workflow are the only ones whose \"very disappointed\" means anything.</p>",
  '<div class="pullquote">Demo-wow gets the signup. Coming back next week is product-market fit. Only measure the second one.</div>',
  "<h2>What \"very disappointed\" looks like for AI</h2>",
  "<p>For an AI product with real fit, the \"very disappointed\" answer sounds like <em>\"this does something I genuinely couldn't do before, or does it 10x faster, and I rely on it now.\"</em> If the open-ended answers are mostly \"it's cool\" or \"fun to play with,\" you have a novelty hit, not fit. The language of dependency — not delight — is what you're listening for.</p>",
  "<h2>How to measure PMF for an AI startup</h2>",
  "<ul>"
  "<li><strong>Survey repeat users only.</strong> Exclude first-session signups; novelty will spike their enthusiasm and lie to you.</li>"
  "<li><strong>Watch retention alongside the score.</strong> If the survey says fit but week-2 retention is collapsing, trust the retention.</li>"
  "<li><strong>Listen for dependency, not delight.</strong> \"I rely on this\" is fit; \"this is amazing\" is a demo reaction.</li>"
  "<li><strong>Validate before you scale.</strong> Cheap to build means easy to build the wrong thing. A 40%+ score is your permission to pour on fuel.</li>"
  "</ul>",
  "<p>AI lowered the cost of building to almost nothing. It didn't lower the cost of building something nobody needs. The PMF score is how you tell the difference before the runway's gone.</p>",
  CTA_END,
 ]),
 faq=[
  ("What's a good PMF score for an AI startup?","40% or more on the Sean Ellis test — there's no AI exception to the benchmark. The catch is measuring it among repeat users who rely on the product, since a great demo inflates first-session enthusiasm that doesn't reflect real fit."),
  ("Why is novelty a problem when measuring AI product-market fit?","Because an impressive AI demo gets people to try once and feel excited, but excitement isn't dependency. If you survey first-session users, novelty will inflate your score. Survey repeat users who've folded the tool into real work to get an honest read."),
  ("Does cheaper AI building change product-market fit?","No — it raises the stakes. When anyone can ship a product in a weekend, building something nobody needs is easier than ever, and \"no market need\" is still the top reason startups fail. Measuring a PMF score is how you confirm there's real demand before scaling."),
 ],
 related=[("/blog/no-market-need-ai-discovery","42% of startups build something nobody wants — and AI is making it worse"),
          ("/blog/how-to-know-if-you-have-product-market-fit","How to know if you have product-market fit: 6 signals"),
          ("/blog/what-is-a-good-pmf-score","What's a good PMF score? The 40% benchmark"),
          ("/pmf-score","Try the free PMF score calculator")],
))

# ---- Developer tools ----
INDUSTRIES.append(dict(
 slug="developer-tools", name="developer tools", kicker="Developer Tools",
 title="PMF Benchmark for Developer Tools: A Good Score | PMFtracker",
 desc="What's a good PMF score for a developer tool? The benchmark is 40% — but stars and signups are vanity. How to measure PMF for dev tools.",
 og="The PMF benchmark for developer tools is 40%. Why GitHub stars are vanity, who your real engaged user is, and how to measure dev-tool PMF.",
 h1="PMF benchmark for developer tools: what's a good product-market fit score?",
 dek="Developer tools are drowning in vanity metrics — stars, signups, Hacker News upvotes. The 40% benchmark cuts through all of it, as long as you survey the one user who matters: the developer who shipped with you.",
 tldr=[
  "The PMF benchmark for developer tools is <strong>40%</strong> — the standard Sean Ellis line.",
  "Stars, signups, and upvotes are vanity. The engaged user is a developer who has <strong>integrated your tool and shipped with it</strong>.",
  "Dev-tool adoption is bottom-up: the developer who uses it daily is your respondent, not the VP who bought the plan.",
  "\"Very disappointed\" for dev tools sounds like \"I'd hate to go back to doing this by hand.\"",
 ],
 body=body([
  "<p>No category has more seductive vanity metrics than developer tools. A thousand GitHub stars, a Hacker News front page, a spike of signups — all of it feels like traction, and none of it tells you whether developers actually depend on your tool. A star costs one click and means nothing. Product-market fit is whether the developer is still using you in production three weeks later.</p>",
  "<p>The benchmark is <strong>40%</strong>, and for dev tools it's a particularly useful reality check against the applause.</p>",
  '<div class="callout"><p class="formula">Is the PMF benchmark different for developer tools? No — it\'s still 40%. It just cuts through the stars-and-signups noise that dev tools accumulate.</p></div>',
  "<h2>Who counts as an engaged user for a dev tool</h2>",
  "<p>Your engaged user is a developer who has <strong>actually integrated the tool and shipped something with it</strong> — it's in their codebase, their pipeline, their workflow. Someone who starred the repo, skimmed the docs, or signed up to try it later hasn't experienced the product. Survey the people who are in production, and your score will tell you something the star count never could.</p>",
  "<h2>Bottom-up adoption changes who you ask</h2>",
  "<p>Developer tools spread bottom-up: an individual developer adopts you, then the team, then eventually someone buys a plan. That means the person whose product-market fit you care about is the <strong>developer using the tool daily</strong>, not the engineering manager who approved the bill. As with B2B SaaS, survey the user, not the buyer — but in dev tools the gap between the two is especially wide.</p>",
  '<div class="pullquote">A GitHub star is a compliment. A developer who\'d be "very disappointed" to lose your tool is product-market fit.</div>',
  "<h2>What \"very disappointed\" looks like for a dev tool</h2>",
  "<p>The fit signal in developer tools is unmistakable when you hear it: <em>\"I'd hate to go back to doing this manually.\"</em> The best dev tools remove a specific, recurring pain — boilerplate, debugging, deployment, glue code — and the developers who'd be devastated to lose you are the ones who remember what life was like before. The open-ended answers will name the exact chore you eliminated. That's your positioning and your roadmap.</p>",
  "<h2>How to measure PMF for a developer tool</h2>",
  "<ul>"
  "<li><strong>Ignore the vanity metrics.</strong> Stars, upvotes, and signups aren't fit. Survey developers who've shipped with the tool.</li>"
  "<li><strong>Survey the user, not the buyer.</strong> The daily-driver developer is your respondent, even if someone else pays.</li>"
  "<li><strong>Listen for the eliminated chore.</strong> \"I'd hate to do this by hand again\" is the dependency you're looking for.</li>"
  "<li><strong>Track it as you grow.</strong> Bottom-up tools can plateau quietly; a tracked score catches stalling fit before revenue does.</li>"
  "</ul>",
  "<p>Developers are a tough, honest audience — they'll happily star a repo and never use it again. The PMF survey is how you find out who's just clapping and who genuinely can't work without you.</p>",
  CTA_END,
 ]),
 faq=[
  ("What's a good PMF score for a developer tool?","40% or more on the Sean Ellis test, measured among developers who've actually integrated and shipped with the tool. Stars, signups, and upvotes are vanity metrics — the score only means something when you survey people running you in production."),
  ("Who should I survey to measure developer-tool product-market fit?","The developers using the tool daily and shipping with it — not the engineering manager who bought the plan, and not people who only starred the repo or signed up. Dev-tool adoption is bottom-up, so the daily-driver developer is your respondent."),
  ("Why aren't GitHub stars a good measure of product-market fit?","Because a star costs one click and signals interest, not dependency. Plenty of starred repos are never used again. Product-market fit is whether developers keep using you in production and would be \"very disappointed\" to lose you — which only a survey of real users reveals."),
 ],
 related=[("/blog/what-is-a-good-pmf-score","What's a good PMF score? The 40% benchmark"),
          ("/blog/how-to-know-if-you-have-product-market-fit","How to know if you have product-market fit: 6 signals"),
          ("/blog/how-to-run-a-pmf-survey","How to run a PMF survey (with the exact questions)"),
          ("/pmf-score","Try the free PMF score calculator")],
))

# ---------------- WRITE INDUSTRY PAGES ----------------
os.makedirs(os.path.join(ROOT,"pmf-benchmark"), exist_ok=True)
written=[]
for d in INDUSTRIES:
    # Cross-link sibling benchmarks (so each page has more than one incoming internal link).
    siblings = [(f"/pmf-benchmark/{x['slug']}", f"PMF benchmark for {x['name']}")
                for x in INDUSTRIES if x["slug"] != d["slug"]][:3]
    related = d["related"][:2] + siblings + [("/pmf-benchmark", "All PMF benchmarks by industry")]
    html = render_article(d["slug"], d["title"], d["desc"], d["og"], d["kicker"], d["h1"], d["dek"],
                          d["tldr"], d["body"], d["faq"], related, d["name"].title())
    path=os.path.join(ROOT,"pmf-benchmark",d["slug"]+".html")
    open(path,"w",encoding="utf-8").write(html)
    written.append(path)

# ---------------- HUB PAGE ----------------
cards=""
HUBCARDS=[
 ("saas","SaaS","Slack, Superhuman, Dropbox — the home turf of the PMF survey. Who to survey and the buyer-vs-user trap."),
 ("fintech","Fintech","Survey funded, active accounts — and why \"very disappointed\" in fintech means trust. How Nubank uses the score."),
 ("marketplace","Marketplaces","Two sides, two scores. Why you measure supply and demand separately, with the Airbnb lesson."),
 ("consumer-apps","Consumer apps","Measure habitual users, not every download. The small-but-mighty core that drives B2C word of mouth."),
 ("ai-startups","AI startups","Demo-wow isn't fit. How to separate novelty from real product-market fit for AI products."),
 ("developer-tools","Developer tools","Stars and signups are vanity. The real engaged user is the developer who shipped with you."),
]
for slug,name,blurb in HUBCARDS:
    cards+=f'''      <a href="/pmf-benchmark/{slug}" class="blog-card">
        <div class="blog-card-tag">Benchmark</div>
        <h2>PMF benchmark for {name}</h2>
        <p>{blurb}</p>
        <span class="blog-card-meta">Read the benchmark →</span>
      </a>

'''
# "Don't see your industry?" request card — opens the email-capture modal (lead.js)
cards += '''      <div class="blog-card lead-request-card">
        <div class="blog-card-tag">Your industry</div>
        <h2>Don't see your industry?</h2>
        <p>Tell us which vertical you're in and we'll build the benchmark for it. Leave your email and we'll send it the moment it's ready.</p>
        <button type="button" class="lead-request-btn" data-lead-open="request">Request your industry →</button>
      </div>

'''

hub_bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":B+"/"},
  {"@type":"ListItem","position":2,"name":"PMF Benchmarks","item":B+"/pmf-benchmark"}]}
hub_items={"@context":"https://schema.org","@type":"ItemList","itemListElement":[
  {"@type":"ListItem","position":i+1,"url":f"{B}/pmf-benchmark/{slug}","name":f"PMF benchmark for {name}"}
  for i,(slug,name,_) in enumerate(HUBCARDS)]}

hub=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>PMF Benchmarks by Industry | PMFtracker</title>
<link href="{B}/pmf-benchmark" rel="canonical"/>
<meta name="description" content="What's a good PMF score in your industry? The benchmark is 40% everywhere — but how you measure it changes. Guides for SaaS, fintech, marketplaces, AI and more."/>
<meta content="PMF Benchmarks by Industry: What's a Good Score?" property="og:title"/>
<meta content="The PMF benchmark is 40% across industries — but who you survey and how you read it changes. Vertical-by-vertical guides to measuring product-market fit." property="og:description"/>
<meta content="{B}/pmf-benchmark" property="og:url"/>
<meta content="https://www.pmftracker.com/images/og-image.avif" property="og:image"/>
<meta property="og:type" content="website"/>
<meta content="summary_large_image" name="twitter:card"/>
<link href="/css/pmftrackerr.webflow.shared.53ff0c310.css" rel="stylesheet" type="text/css"/>
<link href="/css/blog.css" rel="stylesheet" type="text/css"/>
<link href="/images/favicon.png" rel="shortcut icon" type="image/x-icon"/><link href="/images/app-icon.png" rel="apple-touch-icon"/>
{jld(hub_items)}
<link href="/css/site.css" rel="stylesheet" type="text/css"/>

{GTM_HEAD}
<!-- pmf-breadcrumb -->{jld(hub_bc)}</head>
<body class="body blog-page">

{NAV}

<main class="blog-shell">

  <div class="blog-wrap-wide">

    <header class="blog-index-header">
      <span class="blog-eyebrow">PMF Benchmarks by Industry</span>
      <h1>What's a good PMF score in your industry?</h1>
      <p>Here's the honest answer most articles dance around: the product-market fit benchmark is <strong>40%</strong> — the same Sean Ellis line — whether you're building SaaS, fintech, a marketplace, or an AI product. There's no secret different number per vertical. What actually changes by industry is <em>who you survey</em>, what a "very disappointed" answer really means, and the trap that distorts your score. These guides cover both.</p>
    </header>

    <div class="blog-grid">

{cards.rstrip()}

    </div>

    <div class="cta-box" style="margin-top:2.5rem;">
      <h3>Measure your score against the 40% benchmark</h3>
      <p>Whatever your industry, the test is the same. Run the free PMF score calculator and see where you land.</p>
      <a href="/pmf-score" class="cta-btn">Calculate your PMF score →</a>
      <span class="cta-sub">No signup. Built on the Sean Ellis 40% method.</span>
    </div>

  </div>

</main>

{FOOTER}

{GTM_BODY}
</body>
</html>
'''
open(os.path.join(ROOT,"pmf-benchmark","index.html"),"w",encoding="utf-8").write(hub)
written.append(os.path.join(ROOT,"pmf-benchmark","index.html"))

print("WROTE:")
for p in written: print("  ",p.replace(ROOT+"/",""))

# ---------------- KEEP sitemap.xml IN SYNC (idempotent) ----------------
def sync_sitemap():
    sp = os.path.join(ROOT, "sitemap.xml")
    sm = open(sp, encoding="utf-8").read()
    rows = [("/pmf-benchmark", "0.7")] + [(f"/pmf-benchmark/{d['slug']}", "0.6") for d in INDUSTRIES]
    add = ""
    for loc, pri in rows:
        if f"<loc>{B}{loc}</loc>" not in sm:
            add += (f"  <url>\n    <loc>{B}{loc}</loc>\n    <lastmod>2026-06-21</lastmod>\n"
                    f"    <changefreq>monthly</changefreq>\n    <priority>{pri}</priority>\n  </url>\n")
    if add:
        open(sp, "w", encoding="utf-8").write(sm.replace("</urlset>", add + "</urlset>", 1))
    return add.count("<url>")

print(f"sitemap: +{sync_sitemap()} new url(s)")
