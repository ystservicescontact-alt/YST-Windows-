"""Every town we serve, grouped by region.

Each region gets a hub page (/areas/<region>/) and each town a page
(/window-repair-<town>/). Towns that already have a full page in
content.py CITIES are linked to that page instead of getting a new one.
"part" says which municipality a community belongs to (shown on its page).
"""

REGIONS = [
    {
        "slug": "toronto",
        "name": "Toronto",
        "intro": "The City of Toronto has the widest mix of windows in the province: Victorian and Edwardian homes with wood sashes, postwar bungalows, 1990s replacement vinyl windows now reaching the end of their seals, and tens of thousands of condo units with floor-to-ceiling glass and sliding balcony doors.",
        "towns": [
            ("Toronto", ""), ("North York", ""), ("Scarborough", ""), ("Etobicoke", ""),
            ("East York", "part of the City of Toronto"), ("York", "part of the City of Toronto"),
            ("Downtown Toronto", "the downtown core of the City of Toronto"),
            ("Midtown Toronto", "the Yonge and Eglinton, Davisville and Forest Hill area of Toronto"),
            ("East Toronto", "the Leslieville, Danforth and Beaches side of Toronto"),
            ("West Toronto", "the High Park, Roncesvalles and Junction side of Toronto"),
        ],
    },
    {
        "slug": "york-region",
        "name": "York Region",
        "intro": "York Region grew fast from the 1980s on, so many houses here have large casement and picture windows that are now 20 to 40 years old. Foggy sealed units, stripped crank operators and sticking patio doors are the most common calls, from Thornhill up to the shores of Lake Simcoe.",
        "towns": [
            ("Thornhill", "shared by the City of Vaughan and the City of Markham"),
            ("Vaughan", ""), ("Richmond Hill", ""), ("Markham", ""),
            ("Woodbridge", "part of the City of Vaughan"), ("Maple", "part of the City of Vaughan"),
            ("Concord", "part of the City of Vaughan"), ("Kleinburg", "a village in the City of Vaughan"),
            ("Nobleton", "a village in the Township of King"), ("King City", "part of the Township of King"),
            ("Aurora", ""), ("Newmarket", ""), ("East Gwillimbury", ""),
            ("Sharon", "part of the Town of East Gwillimbury"), ("Holland Landing", "part of the Town of East Gwillimbury"),
            ("Queensville", "part of the Town of East Gwillimbury"), ("Georgina", "on the south shore of Lake Simcoe"),
            ("Keswick", "part of the Town of Georgina"), ("Sutton", "part of the Town of Georgina"),
            ("Jackson's Point", "part of the Town of Georgina"), ("Pefferlaw", "part of the Town of Georgina"),
            ("Whitchurch-Stouffville", ""), ("Stouffville", "the main community in Whitchurch-Stouffville"),
            ("Ballantrae", "part of the Town of Whitchurch-Stouffville"),
            ("Unionville", "a heritage community in the City of Markham"), ("Milliken", "part of the City of Markham"),
            ("Buttonville", "part of the City of Markham"), ("Cornell", "part of the City of Markham"),
            ("Cachet", "part of the City of Markham"),
        ],
    },
    {
        "slug": "bradford-simcoe-south",
        "name": "Bradford & Simcoe South",
        "intro": "Bradford West Gwillimbury has added a lot of new subdivisions in the last 20 years. Builder-grade windows in newer homes often have seals and hardware that fail earlier than expected, while older homes in town need glass and crank repairs.",
        "towns": [
            ("Bradford", "the main community in Bradford West Gwillimbury"),
            ("Bradford West Gwillimbury", ""),
        ],
    },
    {
        "slug": "peel",
        "name": "Peel Region",
        "intro": "Peel Region covers Mississauga, Brampton and Caledon, from 1960s neighbourhoods in Bramalea and Cooksville to newer subdivisions and rural properties in Caledon. Older homes need sealed units and hardware; newer homes have more large glass and wide patio doors to maintain.",
        "towns": [
            ("Mississauga", ""), ("Port Credit", "a lakeside community in Mississauga"),
            ("Streetsville", "a historic village in Mississauga"), ("Meadowvale", "part of the City of Mississauga"),
            ("Erin Mills", "part of the City of Mississauga"), ("Cooksville", "part of the City of Mississauga"),
            ("Lakeview", "part of the City of Mississauga"), ("Malton", "part of the City of Mississauga"),
            ("Brampton", ""), ("Bramalea", "part of the City of Brampton"),
            ("Caledon", ""), ("Bolton", "the largest community in the Town of Caledon"),
            ("Palgrave", "a village in the Town of Caledon"), ("Inglewood", "a village in the Town of Caledon"),
            ("Cheltenham", "a village in the Town of Caledon"),
        ],
    },
    {
        "slug": "dufferin-wellington",
        "name": "Dufferin & Wellington",
        "intro": "Dufferin and Wellington counties mix historic stone and brick homes in towns like Elora and Fergus with newer subdivisions in Orangeville and Guelph, plus farm and country properties. Older wood windows need careful glass work, and country homes often have large picture windows facing the view.",
        "towns": [
            ("Orangeville", "in Dufferin County"), ("Shelburne", "in Dufferin County"), ("Mono", "a town in Dufferin County"),
            ("Erin", "a town in Wellington County"), ("Rockwood", "part of the Township of Guelph/Eramosa"),
            ("Fergus", "part of Centre Wellington"), ("Elora", "part of Centre Wellington"), ("Guelph", ""),
        ],
    },
    {
        "slug": "halton",
        "name": "Halton Region",
        "intro": "Halton Region runs from the lakefront in Oakville and Burlington to Milton and Halton Hills. Many homes here were built from the 1980s to the 2010s with large windows, arched transoms and garden doors, and Milton's fast growth means plenty of newer builder-grade windows too.",
        "towns": [
            ("Acton", "part of the Town of Halton Hills"), ("Georgetown", "the largest community in Halton Hills"),
            ("Halton Hills", ""), ("Milton", ""), ("Campbellville", "a village in the Town of Milton"),
            ("Oakville", ""), ("Burlington", ""), ("Waterdown", "part of the City of Hamilton (Flamborough)"),
        ],
    },
    {
        "slug": "hamilton",
        "name": "Hamilton",
        "intro": "Hamilton has older brick homes in the lower city, postwar neighbourhoods on the Mountain, and newer subdivisions in Stoney Creek, Ancaster and Binbrook. Wind off the escarpment and the lake is hard on seals and weatherstripping, so foggy glass and drafty windows are common.",
        "towns": [
            ("Hamilton", ""), ("Stoney Creek", "part of the City of Hamilton"), ("Ancaster", "part of the City of Hamilton"),
            ("Dundas", "part of the City of Hamilton"), ("Flamborough", "part of the City of Hamilton"),
            ("Binbrook", "part of the City of Hamilton (Glanbrook)"),
        ],
    },
    {
        "slug": "niagara",
        "name": "Niagara Region",
        "intro": "Niagara Region has everything from heritage homes in Niagara-on-the-Lake and St. Catharines to newer builds in Grimsby, Lincoln and Welland. Lakefront and escarpment homes get a lot of wind and sun, which wears out seals, caulking and patio door rollers.",
        "towns": [
            ("Grimsby", ""), ("Lincoln", ""), ("Beamsville", "part of the Town of Lincoln"),
            ("Vineland", "part of the Town of Lincoln"), ("Jordan", "a village in the Town of Lincoln"),
            ("St. Catharines", ""), ("Thorold", ""), ("Niagara-on-the-Lake", ""), ("Welland", ""),
            ("Port Colborne", ""), ("Niagara Falls", ""), ("Fort Erie", ""), ("Pelham", ""),
            ("Fonthill", "part of the Town of Pelham"),
        ],
    },
    {
        "slug": "durham",
        "name": "Durham Region",
        "intro": "Durham Region stretches from Pickering and Ajax to Clarington and north to Lake Simcoe. The lakeshore towns have lots of 1980s to 2000s homes whose windows are now failing, while the northern townships have older farmhouses and cottages with their own glass and hardware needs.",
        "towns": [
            ("Ajax", ""), ("Pickering", ""), ("Whitby", ""), ("Brooklin", "part of the Town of Whitby"),
            ("Oshawa", ""), ("Courtice", "part of the Municipality of Clarington"),
            ("Bowmanville", "the largest community in Clarington"), ("Newcastle", "part of the Municipality of Clarington"),
            ("Clarington", ""), ("Port Perry", "part of the Township of Scugog"), ("Uxbridge", ""),
            ("Goodwood", "part of the Township of Uxbridge"), ("Sunderland", "part of the Township of Brock"),
            ("Beaverton", "part of the Township of Brock, on Lake Simcoe"),
        ],
    },
    {
        "slug": "waterloo-brant",
        "name": "Waterloo & Brant",
        "intro": "Kitchener, Waterloo and Cambridge have a mix of older brick homes, 1970s to 1990s subdivisions and many newer townhouses and condos. Brantford, Paris and the surrounding area add heritage homes and country properties. Foggy glass and worn casement hardware are the most common repairs.",
        "towns": [
            ("Kitchener", ""), ("Waterloo", ""), ("Cambridge", ""), ("Ayr", "part of the Township of North Dumfries"),
            ("Brantford", ""), ("Paris", "part of the County of Brant"), ("Simcoe", "in Norfolk County"),
        ],
    },
    {
        "slug": "barrie-simcoe",
        "name": "Barrie & Simcoe County",
        "intro": "Barrie and Simcoe County have grown quickly, with many newer subdivisions in Barrie, Innisfil and New Tecumseth, plus cottages and four-season homes around Lake Simcoe, Wasaga Beach and Collingwood. Cold winters off Georgian Bay and Lake Simcoe are hard on seals and weatherstripping.",
        "towns": [
            ("Barrie", ""), ("Innisfil", ""), ("Alcona", "part of the Town of Innisfil"), ("Angus", "part of the Township of Essa"),
            ("Wasaga Beach", ""), ("Collingwood", ""), ("Stayner", "part of the Township of Clearview"),
            ("Alliston", "part of the Town of New Tecumseth"), ("Tottenham", "part of the Town of New Tecumseth"),
            ("Beeton", "part of the Town of New Tecumseth"), ("Schomberg", "a village in the Township of King"),
            ("Cookstown", "part of the Town of Innisfil"), ("New Tecumseth", ""),
            ("Minesing", "part of the Township of Springwater"), ("Elmvale", "part of the Township of Springwater"),
        ],
    },
]


def town_slug(name):
    s = name.lower().replace("&", "and").replace("'", "").replace(".", "")
    return "window-repair-" + "-".join("".join(ch if ch.isalnum() else " " for ch in s).split())

# Small-town pages are hidden from Google (noindex) until they have something unique.
# A town page is shown to Google when it has a job photo (src/photos/cities/<slug>.jpg)
# or when its name is listed here, e.g. after a real job or review there.
INDEXED_TOWNS = set()
