"""Build the editable Oslo pilot pitch using the approved two-pager and WASTR assets."""

import argparse
from io import BytesIO
from pathlib import Path
import tempfile

import pymupdf
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml import parse_xml
from pptx.util import Pt


ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT.parent / "Wastr.Apps.Web.Landing" / "public"
INK = "20352D"
GREEN = "2F8055"
CORAL = "C84E35"
MINT = "EAF3ED"
SKY = "ECF3F8"
MUTED = "52665B"
RULE = "CEDBD3"
WHITE = "FFFFFF"
NIGHT = "153E2B"
SLIDE_WIDTH = 960
SLIDE_HEIGHT = 540


def text(slide, content, left, top, width, height, size=18, color=INK,
         bold=False, font="Segoe UI", name=None):
    shape = slide.shapes.add_textbox(Pt(left), Pt(top), Pt(width), Pt(height))
    shape.name = name or f"Text {len(slide.shapes)}"
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Pt(0)
    frame.margin_top = frame.margin_bottom = Pt(0)
    frame.vertical_anchor = MSO_ANCHOR.TOP
    for index, line in enumerate(content.split("\n")):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.font.name = font
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = RGBColor.from_string(color)
        paragraph.space_after = Pt(3)
        paragraph.line_spacing = 1.12
    return shape


def block(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(left), Pt(top), Pt(width), Pt(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(color)
    shape.line.fill.background()
    shape._element.spPr.append(parse_xml('<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
    return shape


def picture(slide, path, left, top, width, height):
    shape = slide.shapes.add_picture(str(path), Pt(left), Pt(top), width=Pt(width), height=Pt(height))
    shape.name = Path(path).stem
    return shape


def fitted_image(source, destination, size, focal=(0.5, 0.5)):
    with Image.open(source) as original:
        image = original.convert("RGB")
        scale = max(size[0] / image.width, size[1] / image.height)
        image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
        left = round((image.width - size[0]) * focal[0])
        top = round((image.height - size[1]) * focal[1])
        image.crop((left, top, left + size[0], top + size[1])).save(destination)
    return destination


def standard_slide(presentation, number, label, title):
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(WHITE)
    text(slide, label.upper(), 42, 25, 720, 20, 12, GREEN, True)
    picture(slide, BRAND / "logo_green_white.png", 823, 25, 95, 20.7)
    text(slide, title, 42, 65, 876, 58, 34, INK, font="Bahnschrift", name="Slide title")
    block(slide, 42, 505, 876, 0.75, RULE)
    text(slide, "WASTR  /  OSLO-PILOT  /  OKTOBER 2026", 42, 515, 740, 15, 9, MUTED)
    text(slide, f"{number:02d} / 08", 869, 513, 49, 17, 10, MUTED)
    return slide


def notes(slide, content):
    slide.notes_slide.notes_text_frame.text = content


def prepare_assets(source_deck, asset_dir):
    cover = fitted_image(BRAND / "denis-hero.webp", asset_dir / "cover.jpg", (1920, 1080), (0.5, 0.65))
    with Image.open(cover) as image:
        shading = Image.new("RGBA", image.size)
        painter = ImageDraw.Draw(shading)
        for horizontal in range(image.width):
            opacity = int(170 * max(0, 1 - horizontal / 1650))
            painter.line((horizontal, 0, horizontal, image.height), fill=(12, 34, 23, opacity))
        Image.alpha_composite(image.convert("RGBA"), shading).convert("RGB").save(cover, quality=94)

    with pymupdf.open(source_deck) as source:
        phone_rect = source[3].get_image_rects(54)[0]
        phone_path = asset_dir / "phone.png"
        source[3].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=phone_rect).save(phone_path)
        images = {"phone": phone_path}
        portraits = sorted(
            (image for image in source[6].get_images() if image[2] > 300 and image[3] > 300),
            key=lambda image: source[6].get_image_rects(image[0])[0].x0,
        )
        for label, image_info in zip(("siarhei", "denis", "philip"), portraits, strict=True):
            pixmap = pymupdf.Pixmap(source, image_info[0])
            if image_info[1]:
                pixmap = pymupdf.Pixmap(pixmap, pymupdf.Pixmap(source, image_info[1]))
            output = asset_dir / f"{label}.png"
            with Image.open(BytesIO(pixmap.tobytes("png"))) as original:
                image = original.convert("RGBA")
                bounds = image.getchannel("A").point(lambda value: 255 if value > 240 else 0).getbbox()
                image = image.crop(bounds)
                white = Image.new("RGBA", image.size, "white")
                Image.alpha_composite(white, image).convert("RGB").save(output)
            images[label] = output

    contact_sheet = Image.new("RGB", (1000, 450), "white")
    painter = ImageDraw.Draw(contact_sheet)
    for index, label in enumerate(("phone", "siarhei", "denis", "philip")):
        with Image.open(images[label]) as image:
            image.thumbnail((230, 390), Image.Resampling.LANCZOS)
            contact_sheet.paste(image, (index * 250 + (250 - image.width) // 2, 35))
        painter.text((index * 250 + 20, 10), label, fill="black")
    contact_sheet.save(asset_dir / "asset-check.png")
    images["cover"] = cover
    return images


def build(source_deck, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    asset_dir = Path(tempfile.mkdtemp(prefix="wastr-pitch-"))
    assets = prepare_assets(source_deck, asset_dir)
    presentation = Presentation()
    presentation.slide_width = Pt(SLIDE_WIDTH)
    presentation.slide_height = Pt(SLIDE_HEIGHT)
    presentation.core_properties.title = "WASTR | Forslag til REG-ledet Oslo-pilot"
    presentation.core_properties.subject = "Digital bestilling og dokumentasjon av byggavfall i storsekk"
    presentation.core_properties.author = "WASTR AS"

    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    picture(slide, assets["cover"], 0, 0, 960, 540)
    picture(slide, BRAND / "logo_white.png", 42, 34, 222, 48.4)
    text(slide, "BYGGAVFALL I STORSEKK", 44, 117, 740, 28, 14, WHITE, True)
    text(slide, "Fra bestilling\ntil innsikt.", 40, 157, 650, 175, 62, WHITE, font="Bahnschrift", name="Slide title")
    text(slide, "Forslag til REG-ledet pilot i Oslo", 44, 346, 700, 36, 26, WHITE)
    text(slide, "Åtte uker. Én til to henteoperatører. Målbar læring.", 44, 393, 740, 30, 19, WHITE)
    text(slide, "Til dialog med REG, via Hovinbyen Sirkulære Oslo", 44, 476, 740, 26, 14, WHITE)
    text(slide, "OKTOBER 2026", 44, 512, 700, 17, 10, WHITE)
    text(slide, "Illustrasjon  /  01", 811, 512, 110, 17, 10, WHITE)
    notes(slide, "Visjonen er bedre ordre- og datagrunnlag for små henteoppdrag. Vi foreslår en pilot, ikke en ferdig dokumentert effekt. REGs rolle er ikke avtalt. Tosidig pilotforslag er hoveddokumentet for videresending; dette er det visuelle supplementet.")

    slide = standard_slide(presentation, 2, "Utgangspunktet", "Små oppdrag. Tre ulike behov.")
    columns = [
        (42, "01", "Kunden", "Enklere å bestille", "Hvem henter sekken?\nHva koster det?\nNår blir den hentet?", GREEN),
        (342, "02", "Operatøren", "Mindre manuelt arbeid", "Små oppdrag må registreres,\nplanlegges og følges opp.\nKan dataflyten bli enklere?", CORAL),
        (642, "03", "Kommunen", "Bedre tallgrunnlag", "Hvor mange sekker hentes?\nHvilke fraksjoner?\nHvilke mottak?", GREEN),
    ]
    for left, number, actor, benefit, description, color in columns:
        block(slide, left, 143, 270, 3, color)
        text(slide, number, left, 158, 80, 52, 36, color, font="Bahnschrift")
        text(slide, actor, left, 214, 270, 36, 25, INK, True)
        text(slide, benefit, left, 258, 270, 30, 18, color, True)
        text(slide, description, left, 300, 275, 102, 18, INK)
    block(slide, 0, 421, 960, 70, MINT)
    text(slide, "Kan én strukturert ordre gi verdi for alle tre?", 42, 433, 876, 30, 23, INK, font="Bahnschrift")
    text(slide, "Foreløpige signaler fra aktører i bransjen, ikke dokumenterte funn for hele bransjen.", 42, 468, 876, 21, 12, MUTED)
    notes(slide, "Bakgrunnen er tidlig bransjedialog. Ingen navngitte aktører brukes som referanser eller som om de har godkjent påstandene. Kommunens innsikt skal gjelde registrerte oppdrag i piloten, ikke være et estimat for alt byggavfall i Oslo.")

    slide = standard_slide(presentation, 3, "Løsningen", "Én flyt. To veier inn.")
    with Image.open(assets["phone"]) as phone_image:
        phone_width = 300 * phone_image.width / phone_image.height
    picture(slide, assets["phone"], 70, 146, phone_width, 300)
    text(slide, "Testversjon", 70, 457, 170, 22, 12, MUTED)
    text(slide, "REGISTRER  >  PLANLEGG  >  DOKUMENTER", 270, 137, 648, 25, 13, GREEN, True)
    block(slide, 270, 177, 4, 112, GREEN)
    text(slide, "Operatørens egen kanal", 292, 177, 602, 32, 24, INK, True)
    text(slide, "Bestilling i eget navn (whitelabel). Operatøren beholder\nkunderelasjonen, prisene og egne bestillinger.", 292, 220, 608, 64, 18)
    block(slide, 270, 310, 4, 120, CORAL)
    text(slide, "Nye bestillinger via wastr.no", 292, 310, 602, 32, 24, INK, True)
    text(slide, "WASTR er selger overfor privatkunden. Registrerte\noperatører får tilbud om oppdrag og betalt per oppdrag\nde tar. En mulig kilde til ny etterspørsel.", 292, 353, 608, 80, 18)
    text(slide, "Teknologipartner, ikke renovatør. Operatøren utfører transport og avfallshåndtering.", 270, 455, 645, 40, 13, MUTED)
    notes(slide, "QR-koden åpner en nettbestilling uten app. Registreringen inneholder produkt/fraksjon, sted og bilde. Kartoversikt og rutefordeling hjelper operatøren å planlegge. Kobling til mottakets vekt- og behandlingsdata skal testes; QR-data alene dokumenterer ikke ombruk eller materialgjenvinning. Egne kundeordre trenger ikke deles med konkurrenter. Databruk og tilgang avtales separat for de to kanalene. Produktbildet er hentet fra Denis' testversjon i den vedlagte presentasjonen.")

    slide = standard_slide(presentation, 4, "Pilotmodell", "REG som mulig prosjekteier")
    text(slide, "Til dialog, ikke en avtalt rollefordeling.", 42, 125, 876, 25, 17, MUTED)
    block(slide, 42, 178, 260, 180, MINT)
    text(slide, "REG", 64, 197, 216, 60, 44, GREEN, font="Bahnschrift")
    text(slide, "Definerer kommunens behov\nog ønsket rapportering.\nAvklarer mulig eierskap.", 64, 270, 221, 81, 17)
    text(slide, "+", 324, 231, 50, 62, 42, CORAL, font="Bahnschrift")
    text(slide, "1–2", 408, 178, 240, 88, 66, GREEN, font="Bahnschrift")
    text(slide, "henteoperatører", 408, 272, 280, 38, 25, INK, True)
    text(slide, "Reelle oppdrag på tvers av Oslo.\nNG eller en annen større operatør kan delta\ndersom REG ønsker det, på samme vilkår.", 408, 315, 510, 78, 17)
    block(slide, 42, 411, 876, 3, RULE)
    text(slide, "WASTR", 42, 429, 132, 28, 20, GREEN, True)
    text(slide, "Oppsett, opplæring, støtte, dataflyt og måling.", 187, 430, 730, 28, 19)
    text(slide, "REG forutsettes ikke å hente eller motta avfallet.", 42, 471, 876, 25, 16, CORAL, True)
    notes(slide, "Hovinbyen Sirkulære Oslo kan koble aktørene. WASTR er aktørnøytral; ingen operatør gis særvilkår. REGs kommunale mandat, avfallsansvar, anskaffelseskrav, finansiering og datatilgang må avklares før oppstart. Kommunen får aggregert innsikt etter avtale, ikke innsyn i enkeltkunders bestillinger som standard.")

    slide = standard_slide(presentation, 5, "Forslag til testmål", "Effektivisering skal måles, ikke loves.")
    text(slide, "Ingen målte effekttall ennå. Forslagene er ikke prognoser eller oppnådde resultater.", 42, 126, 876, 28, 16, MUTED)
    measures = [
        (42, "20 %", "lavere tidsbruk", "Minutter per ordre, inkludert\nekstra registrering.", GREEN),
        (342, "10 %", "færre km per henting*", "Kun der operatøren har\nsammenlignbare kjøredata.", CORAL),
        (642, "95 %", "komplette oppdrag", "Avtalte felt for ordre, sted,\nfraksjon, status og\nmottaksreferanse.", GREEN),
    ]
    for left, target, label, description, color in measures:
        text(slide, target, left, 179, 275, 91, 64, color, font="Bahnschrift")
        block(slide, left, 282, 270, 2, RULE)
        text(slide, label, left, 303, 276, 34, 21, INK, True)
        text(slide, description, left, 348, 277, 77, 16)
    text(slide, "*WASTR registrerer foreløpig ikke kjørelengde. Små utvalg gir usikkerhet; uten data gis ingen konklusjon om kjøreeffekt.", 42, 432, 876, 38, 12, MUTED)
    text(slide, "Kommunal innsikt: registrerte sekker per område og periode. Endelige terskler avtales etter førmåling.", 42, 476, 876, 22, 12, GREEN, True)
    notes(slide, "Dette er forslag fra tosidig pitch, ikke tidligere oppnådde resultater. Kjøring vurderes bare der operatøren har brukbare førdata og sammenlignbare ruter. Ta hensyn til volum, avstand og last. 50–100 hentinger er et lite utvalg: en forskjell kan være støy og skal ikke markedsføres som sikker gevinst. Dokumentasjonskrav avtales før test. Mottaksreferanse betyr ikke at behandlingsutfall er verifisert.")

    slide = standard_slide(presentation, 6, "Rammer og innsats", "Åtte uker. Et avgrenset forsøk.")
    timeline = [
        (42, 220, MINT, INK, "UKE 1–2", "Førmåling", "Avgrense oppdrag.\nAvtale datatilgang."),
        (278, 404, NIGHT, WHITE, "UKE 3–6", "Test i faktisk drift", "Anslagsvis 50–100 hentinger totalt.\nJusteres etter faktisk volum."),
        (698, 220, SKY, INK, "UKE 7–8", "Evaluering", "Drift, datakvalitet\nog videre samarbeid."),
    ]
    for left, width, background, foreground, period, heading, description in timeline:
        block(slide, left, 147, width, 143, background)
        text(slide, period, left + 16, 159, width - 32, 22, 12, foreground, True)
        text(slide, heading, left + 16, 190, width - 32, 36, 22, foreground, True)
        text(slide, description, left + 16, 235, width - 32, 48, 16, foreground)
    text(slide, "REG / kommunal partner", 42, 318, 420, 29, 20, GREEN, True)
    text(slide, "Ca. 1 time oppstart\n+ 30 minutter annenhver uke.", 42, 359, 420, 62, 19)
    text(slide, "Operatørens driftskontakt", 510, 318, 408, 29, 20, GREEN, True)
    text(slide, "Ca. 2 timer oppstart + 30 minutter ukentlig.\nOpplæring og registrering kommer i tillegg.", 510, 359, 408, 65, 17)
    text(slide, "SmartOslo: mulig ordning, ikke innvilget støtte.", 42, 442, 876, 28, 18, CORAL, True)
    text(slide, "Oppstart, mandat, kostnader, anskaffelse og databruk avtales. Ressursanslagene avklares med deltakerne.", 42, 480, 876, 21, 12, MUTED)
    notes(slide, "Tidsrammen er åtte uker, ikke tre måneder. Ingen startdato er lovet. REGs innsatsanslag dekker operativ kontakt og oppfølging; eventuell søknads- og prosjekteieradministrasjon må avklares. Per operatør foreslås én driftskontakt, én planlegger og én til to sjåfører. Registrer også merarbeidet løsningen skaper. Filutveksling kan være første integrasjonssteg. Større integrasjoner, betaling, databehandling og ansvar avtales. Ingen ubetinget gratis pilot eller støttebeløp loves.")

    slide = standard_slide(presentation, 7, "Team og modenhet", "Bransje og teknologi. På samme lag.")
    people = [
        (42, "denis", "Denis Pozhinsky", "MEDGRÜNDER / CEO", "20 år fra bygg, anlegg\nog prosjektledelse.", "Multiconsult · AFRY · Metier"),
        (342, "siarhei", "Siarhei Karabitski", "MEDGRÜNDER / CTO", "15+ år med programvare\nog arkitektur.", "Rystad Energy · Vegvesenet · Telenor"),
        (642, "philip", "Philip Hansteen", "RÅDGIVER", "Drift, forretningsutvikling\nog venturekapital.", "Equinor Ventures · Techstars"),
    ]
    for left, asset, full_name, role, experience, companies in people:
        with Image.open(assets[asset]) as portrait:
            portrait_width = 152 * portrait.width / portrait.height
        picture(slide, assets[asset], left, 143, portrait_width, 152)
        text(slide, full_name, left, 308, 284, 31, 23, INK, True)
        text(slide, role, left, 347, 284, 21, 11, GREEN, True)
        text(slide, experience, left, 375, 284, 47, 16)
        text(slide, companies, left, 430, 284, 22, 10, MUTED)
    block(slide, 0, 459, 960, 42, MINT)
    text(slide, "Testversjon klar for demo. B2B-løsningen er i valideringsfase.", 42, 462, 876, 22, 14, GREEN, True)
    text(slide, "B2B-valideringen støttes av Oppstartstilskudd 1 fra Innovasjon Norge, innvilget i mai 2026.", 42, 486, 876, 16, 10, MUTED)
    notes(slide, "WASTR AS ble etablert i 2025. Testversjon for bestilling og operatøroversikt kan demonstreres. B2B-løsningen er i valideringsfase. Integrasjoner, rapportering og driftsgevinster er fortsatt under utprøving. B2B-valideringen støttes av Oppstartstilskudd 1 fra Innovasjon Norge, innvilget i mai 2026. Dette er ikke en opplysning om at SmartOslo har finansiert den foreslåtte piloten. Personbilder og bakgrunn er fra Denis' presentasjon.")

    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(NIGHT)
    picture(slide, BRAND / "logo_white.png", 42, 30, 145, 31.6)
    text(slide, "NESTE STEG", 42, 100, 700, 22, 13, "B8D8C3", True)
    text(slide, "La oss avklare piloten\npå 45 minutter.", 39, 139, 879, 119, 43, WHITE, font="Bahnschrift", name="Slide title")
    text(slide, "Med REG, via Hovinbyen Sirkulære Oslo.\nOperatører inviteres dersom REG ønsker det.", 42, 279, 870, 61, 20, WHITE)
    block(slide, 42, 365, 876, 1, "47715A")
    text(slide, "Vi viser testversjonen og avklarer:", 42, 383, 430, 27, 18, WHITE, True)
    text(slide, "Pilotmodell og kontaktpersoner.\nDatatilgang, kostnader og finansieringsspor.", 42, 425, 460, 57, 17, "D5E5DB")
    text(slide, "Denis Pozhinsky", 566, 382, 352, 31, 23, WHITE, True)
    text(slide, "dep@wastras.com  ·  +47 482 91 492", 566, 424, 352, 26, 16, WHITE)
    text(slide, "wastr.no  ·  zcal.co/wastras", 566, 460, 352, 25, 17, WHITE)
    text(slide, "WASTR AS  ·  ORG.NR. 936 598 536", 42, 515, 700, 16, 10, "B8D8C3")
    text(slide, "08 / 08", 869, 513, 49, 17, 10, "B8D8C3")
    notes(slide, "Be om ett avklaringsmøte, ikke en forhåndsforpliktelse til pilot. Målet er å finne ut om REG ser et kommunalt behov og vil avklare rollen videre. Demoen skal gjøre samtalen konkret. Et eventuelt neste steg må ha avklart mandat, finansiering, datatilgang og ansvar.")

    for slide_number, slide in enumerate(presentation.slides, start=1):
        for shape in slide.shapes:
            if shape.left < 0 or shape.top < 0 or shape.left + shape.width > presentation.slide_width + Pt(1) or shape.top + shape.height > presentation.slide_height + Pt(1):
                raise ValueError(f"Slide {slide_number}: out-of-bounds shape {shape.name}")
    output = output_dir / "2026-10-16_pilot-deck.pptx"
    presentation.save(output)
    reopened = Presentation(output)
    assert len(reopened.slides) == 8
    combined_text = "\n".join(shape.text for slide in reopened.slides for shape in slide.shapes if shape.has_text_frame)
    assert all(value in combined_text for value in ("REG", "SmartOslo", "20 %", "10 %", "95 %", "50–100", "+47 482 91 492"))
    assert not any(value in combined_text for value in ("Regg", "Hento", "Tre måneder", "AI modeller"))
    print(f"PPTX: {output}")
    print(f"ASSET_CHECK: {asset_dir / 'asset-check.png'}")
    print("Verified: 8 slides, required terms and shape boundaries.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-deck", type=Path, default=Path.home() / "Downloads" / "Wastr - HSB.pdf")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "docs" / "stakeholders" / "partners" / "reg" / "materials")
    arguments = parser.parse_args()
    build(arguments.source_deck, arguments.output_dir)