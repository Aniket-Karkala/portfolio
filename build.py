#!/usr/bin/env python3
"""Builds the portfolio pages from data/projects.json.

Run `python3 build.py` after editing the data file. It rewrites index.html,
projects.html, teaching.html, about.html and projects/<slug>.html.
No third-party packages are needed.
"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
P = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
e = html.escape

CATS = [("assistive", "Assistive tech"), ("sensing", "Sensing"), ("robotics", "Robotics and play"),
        ("research", "Research"), ("software", "Software and networks")]
CAT = dict(CATS)
SCALES = [("large", "Large"), ("mid", "Mid-size"), ("small", "Small")]
SCALE = dict(SCALES)
EMAIL = "karkalaaniket@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/aniket-karkala"
GITHUB = "https://github.com/Aniket-Karkala"

ICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231B0E2E'/%3E%3Ccircle cx='16' cy='16' r='9' fill='%23E9B949'/%3E%3Ccircle cx='16' cy='16' r='3.6' fill='%231B0E2E'/%3E%3C/svg%3E"


def scale_mark(s):
    return f'<span class="scale {s}" aria-hidden="true"><i></i><i></i><i></i></span>'


def page(title, desc, body, r="", current="", extra_main_class=""):
    nav = [("index.html", "AK", "home"), ("projects.html", "Projects", "projects"), ("teaching.html", "Teaching", "teaching"),
           ("about.html", "About", "about"), (("" if current == "home" else "index.html") + "#contact", "Contact", "contact")]
    links = "".join(
        f'<a href="{r}{h}"{" class=brand" if k == "home" else ""}{" aria-current=page" if k == current and k != "home" else ""}'
        f'{" aria-label=Home" if k == "home" else ""}>{t}</a>' for h, t, k in nav)
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<!-- Keeps the site out of search engines while it is unlisted. Remove from build.py when you launch. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1B0E2E">
<link rel="icon" href="{ICON}">
<link rel="preload" href="{r}fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="bar" aria-hidden="true"></div>
<div class="glow" aria-hidden="true"></div>
<nav class="nav" aria-label="Main">{links}</nav>
<main id="main"{f' class="{extra_main_class}"' if extra_main_class else ''}>
{body}
</main>
<footer>
  <span>Aniket Karkala, Mumbai</span>
  <span><a href="mailto:{EMAIL}">Email</a> &nbsp; <a href="{LINKEDIN}" rel="noopener">LinkedIn</a> &nbsp; <a href="{GITHUB}" rel="noopener">GitHub</a></span>
</footer>
<script src="{r}js/site.js"></script>
</body>
</html>
"""


def marquee():
    a = ["ESP32", "XIAO ESP32-S3 Sense", "VL53L5CX", "BNO085", "YDLIDAR GS5", "Arduino", "PN532 RFID", "MCP23017", "Load cells",
         "MQ-3 and MQ-135", "ADS1115", "Pogo pins", "GRBL", "ESP-NOW"]
    b = ["C and C++", "Python", "Flask", "Mininet", "Wireshark", "AWS", "MATLAB", "SQL", "LaTeX", "3D printing", "PETG", "Haptics",
         "Wi-Fi dashboards", "Sensor fusion"]
    def row(items, cls=""):
        lis = "".join(f"<li>{e(i)}</li>" for i in items)
        return f'<div class="row{cls}"><ul>{lis}</ul><ul aria-hidden="true">{lis}</ul></div>'
    return f'<div class="parts-band" aria-label="Parts and tools I work with">{row(a)}{row(b, " rev")}</div>'


def contact(r=""):
    return f"""<section class="sec contact" id="contact">
  <h2 class="sec-head">Have something to build?</h2>
  <p data-r>Projects, workshops, mentoring, or a sensor that won't behave. Write to me.</p>
  <a class="mail" href="mailto:{EMAIL}" data-r>{EMAIL}</a>
  <div class="btns" data-r>
    <a class="btn magnet" href="{LINKEDIN}" rel="noopener">LinkedIn</a>
    <a class="btn magnet" href="{GITHUB}" rel="noopener">GitHub</a>
  </div>
  <canvas id="scope" aria-hidden="true"></canvas>
</section>"""


# ------------------------------------------------------------------ home
def home():
    counts = {s: sum(1 for p in P if p["scale"] == s) for s, _ in SCALES}
    blurb = {"large": "Multi-sensor systems, research studies and competition builds that ran for months.",
             "mid": "Complete devices with their own firmware, enclosure and a real problem to solve.",
             "small": "Weekend builds, comparisons and tools that answer one question well."}
    tally = "".join(
        f'<a class="tilt" href="projects.html?scale={s}" data-r style="--d:{i}"><span class="big" data-n="{counts[s]}">{counts[s]}</span>'
        f'<h3>{scale_mark(s)}{e(label)} projects</h3><p>{e(blurb[s])}</p></a>' for i, (s, label) in enumerate(SCALES))
    feat = [p for p in P if p.get("featured")]
    cards = "".join(
        f'<a class="cf-card" href="projects/{p["slug"]}.html" draggable="false"><div><span class="pill">{e(p["role"])}</span>'
        f'<h3>{e(p["name"])}</h3><p>{e(p["tag"])}</p></div><span class="go">Open project</span></a>' for p in feat)
    body = f"""<header class="hero" id="top">
  <h1 class="sr">Aniket Karkala</h1>
  <canvas id="space" aria-hidden="true"></canvas>
  <p class="hint" aria-hidden="true">Move your pointer to orbit</p>
  <div class="hero-copy">
    <p>Robotics engineer and mentor in Mumbai. I build hardware that senses the world, and teach school students to build their own.</p>
    <div class="btns">
      <a class="btn solid magnet" href="projects.html">See all {len(P)} projects</a>
      <a class="btn magnet" href="#contact">Get in touch</a>
    </div>
  </div>
</header>

<section class="sec">
  <h2 class="sec-head">Sensors in, something useful out.</h2>
  <div class="about-grid">
    <div>
      <p class="lead" data-r>I work at Innovation Story in Bandra, where I design embedded and robotics hardware and mentor students from Grade 4 upward through real engineering projects.</p>
      <p data-r style="--d:1">Most of what I build starts with a sensor and a question. Can a cane feel a pothole before a foot does? Can two cheap gas sensors tell a naturally ripened banana from a chemically ripened one? Can a camera decide when a cake is done? I prototype on ESP32 and Arduino boards, print the mechanical parts, and test on the bench until the numbers hold up.</p>
      <div class="btns" data-r style="--d:2"><a class="btn magnet" href="about.html">More about me</a></div>
    </div>
    <div class="tof-wrap" data-r style="--d:1">
      <div class="tof" id="tof" aria-hidden="true"></div>
      <p class="tof-cap">Roughly what an 8×8 time-of-flight imager sees: 64 distances, no picture. Move your pointer around the page. You are the obstacle.</p>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <h2 class="sec-head">{len(P)} projects, three sizes.</h2>
  <div class="tally">{tally}</div>
</section>

{marquee()}

<section class="sec">
  <h2 class="sec-head">A few to start with.</h2>
  <div class="cf-wrap" data-r>
    <div class="cf" tabindex="0" role="group" aria-label="Featured projects. Drag or use the arrow keys."><div class="ring">{cards}</div></div>
    <div class="cf-ctl"><button id="cf-prev" aria-label="Previous project">&#8592;</button><span id="cf-n">1 / {len(feat)}</span><button id="cf-next" aria-label="Next project">&#8594;</button></div>
  </div>
  <div class="btns" style="justify-content:center;margin-top:28px" data-r><a class="btn solid magnet" href="projects.html">Browse every project</a></div>
</section>

<section class="sec" style="padding-top:0">
  <h2 class="sec-head">Teaching is half the job.</h2>
  <div class="tiers">
    <article class="tilt" data-r><span class="big" data-n="40">40</span><h3>hours of electronics, one student at a time</h3><p>Fifteen projects in three tiers on ESP32-S3 and ESP32-C3 boards.</p></article>
    <article class="tilt" data-r style="--d:1"><span class="big" data-n="12">12</span><h3>modules in a one-day ESP32 workshop</h3><p>From a blinking LED to a Wi-Fi dashboard, for Grade 10 students.</p></article>
    <article class="tilt" data-r style="--d:2"><span class="big" data-n="2">2</span><h3>handbooks written for Grade 4 and 5</h3><p>So young students understand every part of the robot they are building.</p></article>
  </div>
  <div class="btns" style="margin-top:28px" data-r><a class="btn magnet" href="teaching.html">See how I teach</a></div>
</section>

{contact()}"""
    return page("Aniket Karkala, robotics engineer and mentor",
                "Aniket Karkala is a robotics engineer and mentor in Mumbai who builds sensor-heavy embedded hardware and teaches school students to build their own.",
                body, current="home")


# ------------------------------------------------------------------ projects index
def index():
    chips = '<button class="chip" data-k="cat" data-v="all">All types</button>' + "".join(
        f'<button class="chip" data-k="cat" data-v="{k}">{e(v)}</button>' for k, v in CATS)
    sizes = '<button class="chip" data-k="scale" data-v="all">Any size</button>' + "".join(
        f'<button class="chip" data-k="scale" data-v="{k}">{e(v)}</button>' for k, v in SCALES)
    cards = ""
    for i, p in enumerate(P):
        text = " ".join([p["name"], p["tag"], p["role"], CAT[p["cat"]], *p["in"], *p["core"], *p["out"]]).lower()
        cards += (f'<a class="card tilt" href="projects/{p["slug"]}.html" data-cat="{p["cat"]}" data-scale="{p["scale"]}" data-text="{e(text)}" '
                  f'data-r style="--d:{i % 3};view-transition-name:c-{p["slug"]}">'
                  f'<div class="meta"><span class="pill">{scale_mark(p["scale"])}{e(SCALE[p["scale"]])}</span><span class="pill">{e(CAT[p["cat"]])}</span></div>'
                  f'<h3>{e(p["name"])}</h3><p>{e(p["tag"])}</p><div class="meta"><span class="pill gold">{e(p["role"])}</span></div></a>')
    body = f"""<header class="page-head">
  <h1 class="sec-head" style="max-width:none">Things I've built and helped build.</h1>
  <p class="lead" data-r>{len(P)} projects, from weekend builds to months-long research. Open any one for how it works, what is inside it and what went wrong along the way.</p>
</header>
<div class="tools" data-r>
  <div role="group" aria-label="Filter by type">{chips}</div>
  <div role="group" aria-label="Filter by size">{sizes}</div>
  <div><label class="sr" for="q">Search projects</label><input class="search" id="q" type="search" placeholder="Search parts or names"></div>
</div>
<p class="count" id="count" aria-live="polite">{len(P)} projects</p>
<div class="grid" id="grid">{cards}</div>
<p class="empty" id="empty" hidden>No projects match those filters. Clear the search or choose "All types".</p>"""
    return page("Projects, Aniket Karkala", "Robotics, sensing, research and software projects built or mentored by Aniket Karkala.", body, current="projects")


# ------------------------------------------------------------------ project page
def project(i):
    p = P[i]; prev, nxt = P[i - 1], P[(i + 1) % len(P)]
    plates = "".join(
        f'<div class="plate p{k}" style="--k:{k - 1}"><b>{t}</b>{"".join(f"<span>{e(x)}</span>" for x in p[key])}</div>'
        for k, (t, key) in enumerate([("Inputs", "in"), ("Core", "core"), ("Outputs", "out")]))
    flow = "".join(
        f'<div data-r style="--d:{k}"><h3>{t}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in p[key])}</ul></div>'
        for k, (t, key) in enumerate([("Inputs", "in"), ("Core", "core"), ("Outputs", "out")]))
    steps = "".join(f'<li data-r style="--d:{k}">{e(s)}</li>' for k, s in enumerate(p["how"]))
    notes = ""
    if p["notes"]:
        notes = f"""<section class="sec tight"><div class="two">
  <h2 class="sec-head" style="font-size:clamp(1.9rem,4vw,3.2rem)">What I learned building it.</h2>
  <ul class="notes">{"".join(f'<li data-r style="--d:{k}">{e(n)}</li>' for k, n in enumerate(p["notes"]))}</ul>
</div></section>"""
    body = f"""<header class="proj-hero">
  <div>
    <a class="crumb" href="../projects.html">&#8592; All projects</a>
    <h1 style="view-transition-name:c-{p["slug"]}">{e(p["name"])}</h1>
    <p class="lead" data-r>{e(p["tag"])}</p>
    <div class="meta" data-r style="--d:1"><span class="pill gold">{e(p["role"])}</span><span class="pill">{scale_mark(p["scale"])}{e(SCALE[p["scale"]])} project</span><span class="pill">{e(CAT[p["cat"]])}</span></div>
  </div>
  <div class="stack" aria-hidden="true"><div class="stack-in">{plates}</div></div>
</header>

<section class="sec tight"><div class="two">
  <h2 class="sec-head" style="font-size:clamp(1.9rem,4vw,3.2rem)">The problem.</h2>
  <p class="lead" style="max-width:38ch" data-r>{e(p["problem"])}</p>
</div></section>

<section class="sec tight">
  <h2 class="sec-head" style="font-size:clamp(1.9rem,4vw,3.2rem)">What is inside.</h2>
  <div class="flow"><i class="wire" aria-hidden="true"></i>{flow}</div>
</section>

<section class="sec tight"><div class="two">
  <h2 class="sec-head" style="font-size:clamp(1.9rem,4vw,3.2rem)">How it works.</h2>
  <ol class="steps">{steps}</ol>
</div></section>

{notes}

<nav class="nextprev" aria-label="More projects">
  <a href="{prev["slug"]}.html"><small>Previous</small><b>{e(prev["name"])}</b></a>
  <a href="{nxt["slug"]}.html"><small>Next</small><b>{e(nxt["name"])}</b></a>
</nav>"""
    return page(f'{p["name"]}, Aniket Karkala', p["tag"], body, r="../", current="projects")


# ------------------------------------------------------------------ teaching
def teaching():
    mods = [("Meet the microcontroller", "What a microcontroller is and a tour of the board."),
            ("Set up the Arduino IDE", "Install, select the board, upload the first sketch."),
            ("Digital output", "Blink, LED chaser, traffic light and a binary counter."),
            ("Digital input", "Buttons, pull-ups, debouncing and a reaction-time game."),
            ("Sound", "Buzzer tones and programming a melody."),
            ("Analog input", "Potentiometer, light sensor and hysteresis."),
            ("PWM and colour", "Dimming and mixing colours on an RGB LED."),
            ("Sensors", "Capacitive touch, temperature and humidity, ultrasonic distance."),
            ("Doing two things at once", "Timing with millis() and simple state machines."),
            ("Interrupts", "Reacting to events the moment they happen."),
            ("Wi-Fi dashboard", "A web server on the board, in access-point mode."),
            ("Capstone build", "Students pick a project from a menu and are graded on a rubric.")]
    mod_html = "".join(f'<li data-r style="--d:{i % 4}"><b>{e(a)}</b><span>{e(b)}</span></li>' for i, (a, b) in enumerate(mods))
    body = f"""<header class="page-head">
  <h1 class="sec-head" style="max-width:none">Teaching is half the job.</h1>
  <p class="lead" data-r>I mentor school students from Grade 4 to Grade 10. Every course below was written for real sessions and rewritten after them.</p>
</header>

<section class="sec tight">
  <h2 class="sec-head">One day, twelve modules.</h2>
  <p data-r>ESP32 Fundamentals is a full-day, hands-on workshop for Grade 10 students. It comes with a mentor handbook, an 81-slide student deck, a quiz after each module and a 20-question final. One pin map is used all day, so circuits build up on a single breadboard instead of being torn down between modules.</p>
  <ol class="modules" style="margin-top:28px">{mod_html}</ol>
</section>

<section class="sec tight">
  <h2 class="sec-head">Forty hours, fifteen projects.</h2>
  <p data-r>A one-to-one electronics course for a Grade 8 student who already knew basic C. It runs on ESP32-S3 and ESP32-C3 boards and comes with a 28-slide student guide and a mentor's reference with annotated code and wiring diagrams for every project.</p>
  <div class="tiers" style="margin-top:28px">
    <article class="tilt" data-r><span class="big">8</span><h3>foundation projects</h3><ul><li>NeoPixel animations</li><li>Native USB</li><li>Bluetooth beacons</li><li>Deep sleep</li><li>MQTT messaging</li><li>Over-the-air updates</li><li>Capacitive touch piano</li><li>Bluetooth proximity</li></ul></article>
    <article class="tilt" data-r style="--d:1"><span class="big">4</span><h3>intermediate projects</h3><ul><li>Gesture-controlled display</li><li>Bluetooth mesh network</li><li>USB keyboard emulation</li><li>WebSocket dashboard</li></ul></article>
    <article class="tilt" data-r style="--d:2"><span class="big">3</span><h3>capstone options</h3><ul><li>Hand-sign detection</li><li>Security camera with phone alerts</li><li>Bluetooth health band</li></ul></article>
  </div>
</section>

<section class="sec tight"><div class="two">
  <h2 class="sec-head" style="font-size:clamp(1.9rem,4vw,3.2rem)">Handbooks for the youngest builders.</h2>
  <div>
    <p class="lead" style="max-width:36ch" data-r>For a World Robot Olympiad build I wrote two books for Grade 4 and 5 students.</p>
    <p data-r style="--d:1">The first is a 20-chapter general volume with a custom diagram for every module, story dialogue, quick-fact tables and mini quizzes. The second is a 25-page deep-dive that explains the real values in the team's own firmware: bus speeds, RFID frequency, servo pulse counts and timing constants.</p>
    <div class="btns" data-r style="--d:2"><a class="btn magnet" href="projects/smart-temple.html">See the Smart Temple project</a></div>
  </div>
</div></section>

<section class="sec tight"><div class="two">
  <h2 class="sec-head" style="font-size:clamp(1.9rem,4vw,3.2rem)">How I run a project.</h2>
  <ul class="notes">
    <li data-r>One sensor at a time. Every part is tested alone on the bench before anything is integrated.</li>
    <li data-r style="--d:1">Real data early. Students log readings by hand first, so they know what a number means before code hides it.</li>
    <li data-r style="--d:2">Hours, not dates. Research projects are planned as hour budgets with gates, because school calendars slip.</li>
    <li data-r style="--d:3">Honest claims. A screening tool is called a screening tool, and limits go in the report.</li>
  </ul>
</div></section>

{contact()}"""
    return page("Teaching, Aniket Karkala", "Courses, workshops and handbooks Aniket Karkala has written for school students.", body, current="teaching")


# ------------------------------------------------------------------ about
def about():
    body = f"""<header class="page-head">
  <h1 class="sec-head" style="max-width:none">Measure first, then change one thing.</h1>
</header>

<section class="sec tight">
  <div class="about-grid">
    <div>
      <p class="lead" data-r>I'm Aniket, a robotics engineer and mentor at Innovation Story in Bandra, Mumbai.</p>
      <p data-r style="--d:1">I design embedded and robotics hardware and mentor school students through engineering projects for science fairs and robotics competitions. Most of my builds start with a sensor and a question, run on ESP32 or Arduino boards, and end up in a 3D-printed enclosure on a test bench.</p>
      <p data-r style="--d:2">I trained as an electronics and telecommunication engineer with a minor in IoT, and spent my internships at Reliance Jio working on network security and cloud. That background shows up in how I debug.</p>
      <div class="btns" data-r style="--d:3"><a class="btn solid magnet" href="projects.html">See the projects</a><a class="btn magnet" href="mailto:{EMAIL}">Email me</a></div>
    </div>
    <div class="tof-wrap" data-r style="--d:1">
      <div class="tof" id="tof" aria-hidden="true"></div>
      <p class="tof-cap">An 8×8 time-of-flight view of your pointer.</p>
    </div>
  </div>
</section>

<section class="sec tight">
  <h2 class="sec-head">Where I've worked and studied.</h2>
  <ol class="xp" id="xp">
    <li data-r><time>Nov 2025 to now</time><h3>Robotics Engineer and Mentor</h3><p class="where">Innovation Story, Bandra, Mumbai</p><p>I mentor school students through engineering projects for science fairs and robotics competitions, build the embedded prototypes behind them, and write the courses and handbooks we teach from.</p></li>
    <li data-r><time>Jun to Jul 2024</time><h3>Network Engineer Intern</h3><p class="where">Reliance Jio, Navi Mumbai</p><p>Designed and analysed DDoS attacks in software-defined networks and built mitigation that cut packet drop during attacks by 94%.</p></li>
    <li data-r><time>Jun to Jul 2024</time><h3>AWS Cloud Solution Architect Intern</h3><p class="where">Reliance Jio, Navi Mumbai</p><p>Built a demo storefront and designed its hosting on EC2, DynamoDB, Lambda and S3.</p></li>
    <li data-r><time>Graduated 2025</time><h3>B.E. Electronics and Telecommunication</h3><p class="where">Vidyalankar Institute of Technology, Mumbai</p><p>Minor in Internet of Things. CGPI 9.89 out of 10.</p></li>
  </ol>
</section>

<section class="sec tight">
  <h2 class="sec-head">What I work with.</h2>
  <div class="skills">
    <div data-r><h3>Boards</h3><ul><li>ESP32</li><li>ESP32-S3</li><li>ESP32-C3</li><li>XIAO ESP32-S3 Sense</li><li>Arduino Uno, Nano, Leonardo</li><li>micro:bit</li></ul></div>
    <div data-r style="--d:1"><h3>Sensing</h3><ul><li>Lidar</li><li>Time-of-flight</li><li>IMUs</li><li>Gas sensors</li><li>Load cells</li><li>Force sensors</li><li>RFID</li><li>Cameras</li></ul></div>
    <div data-r style="--d:2"><h3>Software</h3><ul><li>C and C++</li><li>Python</li><li>SQL</li><li>MATLAB</li><li>Flask</li><li>HTML, CSS, JavaScript</li><li>LaTeX</li></ul></div>
    <div data-r style="--d:3"><h3>Networks and cloud</h3><ul><li>Mininet</li><li>SDN</li><li>Wireshark</li><li>sFlow-RT</li><li>AWS</li><li>ESP-NOW</li><li>MQTT</li></ul></div>
    <div data-r><h3>Making</h3><ul><li>3D printing</li><li>PETG parts</li><li>GRBL and CNC</li><li>Soldering</li><li>Pogo-pin joints</li></ul></div>
    <div data-r style="--d:1"><h3>Certificates</h3><ul><li><a href="https://www.credly.com/badges/929f06ec-ffab-48f6-9978-54bdf09b9d6a/public_url" rel="noopener">AWS Cloud Foundations</a></li><li><a href="https://www.credly.com/badges/ae2c43a5-6c79-4603-aaaa-43f4bc6d30e6/public_url" rel="noopener">Cisco Networking Basics</a></li></ul></div>
  </div>
</section>

{marquee()}
{contact()}"""
    return page("About, Aniket Karkala", "Background, experience and skills of Aniket Karkala, robotics engineer and mentor in Mumbai.", body, current="about")


def main():
    (ROOT / "projects").mkdir(exist_ok=True)
    for old in (ROOT / "projects").glob("*.html"):
        old.unlink()
    (ROOT / "index.html").write_text(home(), encoding="utf-8")
    (ROOT / "projects.html").write_text(index(), encoding="utf-8")
    (ROOT / "teaching.html").write_text(teaching(), encoding="utf-8")
    (ROOT / "about.html").write_text(about(), encoding="utf-8")
    for i in range(len(P)):
        (ROOT / "projects" / f'{P[i]["slug"]}.html').write_text(project(i), encoding="utf-8")
    print(f"Built 4 pages and {len(P)} project pages.")


if __name__ == "__main__":
    main()
