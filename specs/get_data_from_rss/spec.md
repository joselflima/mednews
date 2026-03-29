# Spec: Get data from RSS

## Description

This module is responsible for fetching data from medical RSS feeds. By now, the module should be able to fetch data from the following RSS feeds:
- Medical Xpress (https://medicalxpress.com/rss-feed/)

## Acceptance Criteria

- [] When called, the module should fetch data from the RSS feeds.
- [] After getting the data, the module should return the entries from feedparser.
- [] The module must return a clean and separated data from RSS XML file.

## Tests

- [] When called, the module should receive a XML format data.
- [] Answer must have at least the future fields: **title**, **description**, **link**, **pubDate**
- [] If we have a fail to fetch the data, the module should thrown an exception (error handling).

## Expected XML format from RSS

- Medical Xpress:

```xml
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
    <channel>
        <title>
        Medical Xpress - latest medical and health news stories
        </title>
        <link>https://medicalxpress.com/</link>
        <language>en-us</language>
        <description>
        Medical Xpress internet news portal provides the latest news on science including: Physics, Nanotechnology, Life Sciences, Space Science, Earth Science, Environment, Health and Medicine.
        </description>
        <item>
            <title>
            Five ways future health care leaders can tackle burnout in the workforce
            </title>
            <description>
            The fight against widespread burnout in the health care workforce should begin with the training of future health care administrators, according to a new paper from the George Mason University College of Public Health. Published in the Journal of Health Administration Education, the paper examines how health administration programs can better prepare future leaders to address burnout by focusing on workplace factors such as working conditions, leadership support, job design and workload, social connections, and opportunities for advancement.
            </description>
            <link>
            https://medicalxpress.com/news/2026-03-ways-future-health-leaders-tackle.html
            </link>
            <category/>
            <pubDate>Sun, 29 Mar 2026 15:30:02 EDT</pubDate>
            <guid isPermaLink="false">news693580973</guid>
            <media:thumbnail url="https://scx1.b-cdn.net/csz/news/tmb/2022/stressed-nurse.jpg" width="90" height="90"/>
        </item>
        <item>
            <title>
            How gene-targeting technology is transforming STI diagnosis
            </title>
            <description>
            Most people who have heard of clustered regularly interspaced short palindromic repeats (more commonly known as CRISPR) associate it with gene editing—the precise molecular scissors that allow scientists to cut and rewrite DNA. But the same underlying technology that makes CRISPR so powerful for editing genes also makes it a versatile diagnostic tool.
            </description>
            <link>
            https://medicalxpress.com/news/2026-03-gene-technology-sti-diagnosis.html
            </link>
            <category/>
            <pubDate>Sun, 29 Mar 2026 14:30:01 EDT</pubDate>
            <guid isPermaLink="false">news693564629</guid>
            <media:thumbnail url="https://scx1.b-cdn.net/csz/news/tmb/2026/how-gene-targeting-tec.jpg" width="90" height="90"/>
        </item>
        <item>
            <title>
            First functional brain atlas shows how communication networks change from infancy to old age
            </title>
            <description>
            If you want to know more about how the human brain matures and changes over time, you can now consult the first comprehensive atlas that maps brain organization from infancy all the way through to advanced old age. To create this comprehensive guide, researchers analyzed brain scans from 3,556 healthy individuals, ranging from newborns who were just 16 days old to centenarians. They used a technique called resting-state fMRI to see which parts of the brain communicate with each other while a person is lying still.
            </description>
            <link>
            https://medicalxpress.com/news/2026-03-functional-brain-atlas-communication-networks.html
            </link>
            <category/>
            <pubDate>Sun, 29 Mar 2026 14:00:01 EDT</pubDate>
            <guid isPermaLink="false">news693754271</guid>
            <media:thumbnail url="https://scx1.b-cdn.net/csz/news/tmb/2026/first-functional-brain.jpg" width="90" height="90"/>
        </item>
    </channel>
</rss>
