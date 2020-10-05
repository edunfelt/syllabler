import json


class SyllablerModel(object):
    """Syllabler model for auto generated texts"""

    def __init__(self):
        """New course data"""
        self.texts = {}
        self.data = {}

    def read_data(self, data):
        data_file = open(data)
        self.data = json.load(data_file)

    def eligibility(self):
        """Auto generate eligibility text"""
        if self.data["eligibility"] == "Grundläggande behörighet":
            self.texts["11. Behörighet"] = "Inget - Grundläggande behörighet <br>"
        elif self.data["eligibility"] == "Särskild behörighet":
            self.texts["11. Behörighet"] = "För tillträde till kursen krävs kunskaper motsvarande " \
                                           + self.data["requirements"] + ".<br>"
        elif self.data["level"] == "Grundnivå" and self.data["eligibility"] == "Självständigt arbete":
            self.texts["11. Behörighet"] = "För tillträde till självständigt arbete krävs minst 135 hp.<br>"
        elif self.data["level"] == "Avancerad nivå" and self.data["eligibility"] == "Självständigt arbete":
            self.texts["11. Behörighet"] = "För tillträde till självständigt arbete på avancerad nivå krävs kunskaper " \
                                           "motsvarande avlagd kandidatexamen, samt minst 15 hp på avancerad nivå. GB " \
                                           "får medge undantag från dessa krav för självständiga arbeten som ingår i " \
                                           "program som leder till yrkesexamen. <br>"

    def course_desc(self):
        """Auto generate course description text"""
        number_of_parts = 0
        desc_text_b = ""
        contents = self.data["description"].split(", ")
        contents_formatted = ""
        for line in contents:
            contents_formatted += "- " + line + "<br>"

        if self.data["parts"] != 0:
            for title, text in self.data.items():
                if title[:5] == "part_":
                    number_of_parts += 1
                    part_text = "Del " + str(number_of_parts) + ", "
                    for key, value in text.items():
                        if key == "part_name":
                            part_text += value + ", "
                        elif key == "part_credits":
                            part_text += value + " hp"
                    desc_text_b += part_text + "<br>"
            self.texts["12. Kursens innehåll"] = "a. Kursen behandlar<br>" + contents_formatted \
                                             + "<br><br>" + "b. Kursen består av följande delar: <br>" + desc_text_b
        else:
            self.texts["12. Kursens innehåll"] = "a. Kursen behandlar<br>" + contents_formatted

    def expected_results(self):
        """Auto generate text for expected results"""
        number_of_parts = 0
        expected_text = ""
        if self.data["parts"] != 0:
            for title, text in self.data.items():
                if title[:5] == "part_":
                    number_of_parts += 1
                    expected_text += "Del " + str(number_of_parts) + ", " + text["part_name"] \
                                     + ", " + text["part_credits"] + " hp:<br>"
                    for key, value in text.items():
                        if key == "part_goal":
                            goal_text = value
                            goals = goal_text.split(", ")
                            for goal in goals:
                                expected_text += "- " + goal + "<br>"
            self.texts["13. Förväntade studieresultat"] = "Efter att ha genomgått kursen förväntas studenten kunna: <br>" \
                                                      + expected_text
        else:
            self.texts["13. Förväntade studieresultat"] = "Efter att ha genomgått kursen förväntas studenten kunna " \
                                                          "(lista över resultat)..."

    def teaching(self):
        """Auto generated text for teaching options"""
        teaching_options = ""
        for title, text in self.data.items():
            if title[:8] == "teaching":
                if text != "":
                    teaching_options += title.lstrip("teaching_").lower() + ", "
            elif title == "online_course" and text == "Ja":
                teaching_options += "<br><br>Undervisning sker på distans."
        teaching_options += "<br><br>Kursens undervisningsspråk anges inför varje kurstillfälle och framgår av den " \
                            "digitala utbildningskatalogen.<br>"

        if self.data["eligibility"] == "Självständigt arbete":
            self.texts["14. Undervisning"] = "Handledning av självständiga arbetem och examensarbeten: <br>" \
                                             + "Studenten har rätt till minst XX timmars handledning, där individuell " \
                                               "handledning ska utgöra minst en tredjedel av tiden.<br>" \
                                             + "Handledning ges endast inom den planerade kurstiden. Vid särskilda " \
                                               "omständigheter kan studenten beviljas förlängd handledartid. Begäran " \
                                               "om detta ska ställas till institutionsstyrelsen. <br><br>" \
                                             + "Rätt att byta handledare:<br>" \
                                             + "Vid särskilda omständigheter har studenten rätt att byta handledare. " \
                                               "Begäran om detta ska ställas till institutionsstyrelsen.<br>"
        else:
            self.texts["14. Undervisning"] = "Undervisningen består av " + teaching_options

    def examination_a(self):
        """Auto generated text for course examination"""
        number_of_parts = 0
        text_part_a = "a. Kursen examineras på följande vis: <br>"

        if self.data["parts"] != 0:
            for title, text in self.data.items():
                if title[:5] == "part_":
                    number_of_parts += 1
                    text_part_a += "Kunskapskontroll för del " + str(number_of_parts) \
                                   + " sker genom " + text["part_exam"].lower() + ".<br>"
        else:
            text_part_a += "Kunskapskontroll sker genom..."

        text_part_a += "<br>Examinator har möjlighet att besluta om anpassad eller alternativ examination " \
                       "för studenter med funktionsnedsättning. "

        return text_part_a + "<br><br>"

    def examination_b(self):
        text_part_b = "b. För godkänt slutbetyg krävs deltagande i "
        for title, text in self.data.items():
            if title[:4] == "task" and text != "":
                text_part_b += title.lstrip("task_").lower() + ", "
        text_part_b += ". Om särskilda skäl föreligger kan examinator efter samråd med vederbörande lärare medge den " \
                       "studerande befrielse från skyldigheten att delta i viss obligatorisk undervisning.<br>"

        return text_part_b + "<br>"

    def examination_c(self):
        number_of_parts = 0
        required_part = ""
        text_part_c = ""
        if self.data["grading_scale"] == "AF - sjugradig skala":
            text_part_c += "c. Betygsättning: Kursens betyg sätts enligt sjugradig målrelaterad skala:<br> A = " \
                           "Utmärkt<br> B = Mycket bra<br> " \
                           "C = Bra<br> D = Tillfredsställande<br> E = Tillräckligt<br> Fx = Underkänd, något mer arbete " \
                           "krävs<br> F = Underkänd, mycket mer arbete krävs<br>"
        elif self.data["grading_scale"] == "UV - tregradig skala":
            text_part_c += "c. Betygsättning: Kursens slutbetyg sätts enligt tregradig målrelaterad skala:<br> V = Väl " \
                           "godkänd<br> G = Godkänd<br> U = Underkänd<br>"
        else:
            text_part_c += "c. Betygsättning: Kursens slutbetyg sätts enligt tvågradig målrelaterad skala:<br> G = " \
                           "Tillfredsställande<br> U = Underkänd<br>"

        for title, text in self.data.items():
            if title[:5] == "part_":
                number_of_parts += 1

                if text["part_grading"] == "AF - sjugradig":
                    part_grading = "sjugradig målrelaterad skala"
                elif text["part_grading"] == "UV - tregradig":
                    part_grading = "tregradig skala underkänd (U), godkänd (G), väl godkänd (VG)"
                else:
                    part_grading = "tvågradig betygsskala: underkänd (U) eller godkänd (G)"

                text_part_c += "<br>Betygsättning av del " + str(number_of_parts) \
                               + " sker enligt " + part_grading + "."
                if text["part_required"] != "":
                    required_part += " del " + str(number_of_parts) + ","
        text_part_c += "<br><br>För godkänt betyg krävs godkänt betyg på samtliga ingående delar.<br>"
        if self.data["weighted"] != "":
            text_part_c += "<br>Kursens slutbetyg sätts genom en sammanvägning av betygen på kursens delar, " \
                           "där de olika delarnas betyg viktas i förhållande till deras omfattning.<br>"
        if required_part != "":
            text_part_c += "<br>Kursens slutbetyg sätts utifrån betygsättning på" + required_part + ".<br>"

        return text_part_c + "<br>"

    def examination_d(self):
        text_part_d = "d. "
        if self.data["eligibility"] == "Självständigt arbete":
            text_part_d += "Grundläggande bedömningsgrunder är:<br> 1. Förståelse för den förelagda uppgiften<br> 2. " \
                           "Genomförande av experimenten<br> 3. Kunskap om den teoretiska bakgrunden<br> 4. Tolkning och " \
                           "analys av resultat<br> 5. Självständighet<br> 6. Förmåga att hålla den fastställda tidsplanen " \
                           "för arbetet<br> 7. Presentation - muntlig redovisning<br> 8. Presentation - skriftlig " \
                           "redovisning<br> 9. Övrigt<br>"
        else:
            text_part_d += "Kursens betygskriterier delas ut vid kursstart.<br>"

        return text_part_d + "<br>"

    def examination_f(self):
        text_part_f = "f. "
        if self.data["completion"] == "Komplettering Fx till E":
            text_part_f += "Vid betyget Fx ges möjlighet att komplettera upp till betyget E. Examinator beslutar om " \
                           "vilka kompletteringsuppgifter som ska utföras och vilka kriterier som ska gälla för att " \
                           "bli godkänd på kompletteringen. Kompletteringen ska äga rum före nästa " \
                           "examinationstillfälle. "
        elif self.data["completion"] == "Komplettering Fx till A-E":
            text_part_f += "Vid betyget Fx ges möjlighet att komplettera till godkänt betyg. Examinator beslutar om " \
                           "vilka kompletteringsuppgifter som ska utföras ochvilka kriterier som ska gälla för att " \
                           "bli godkänd på kompletteringen. Kompletteringen ska äga rum före nästa " \
                           "examinationstillfälle. Vid godkänd komplettering av brister av förståelsekaraktär -mindre " \
                           "missförstånd, smärre felaktigheter eller i någon del alltför begränsade resonemang " \
                           "-används betyget E. Vid godkänd komplettering av enklare formaliafel används betygen A-E. "
        elif self.data["completion"] == "Komplettering U till G":
            text_part_f += "Vid betyget U ges möjlighet att komplettera upp till betyget G.Examinator beslutar om " \
                           "vilka kompletteringsuppgifter som ska utförasoch vilka kriterier som ska gälla för att " \
                           "bli godkänd på kompletteringen. Kompletteringen ska äga rum före nästa " \
                           "examinationstillfälle. "
        elif self.data["completion"] == "Ej komplettering Fx till E":
            text_part_f += "Möjlighet till komplettering av betyget Fx upp till godkänt betyg ges inte pådenna kurs."
        else:
            text_part_f += "Möjlighet till komplettering av betyget U upp till godkänt betyg ges inte på denna kurs."

        return text_part_f + "<br><br>"

    def examination(self):
        self.texts["15. Kunskapskontroll och examination"] = self.examination_a() + self.examination_b() \
                                                             + self.examination_c() + self.examination_d() \
                                                             + "e. Studerande som underkänts i ordinarie prov har rätt " \
                                                               "att genomgå ytterligare prov så länge kursen ges. " \
                                                               "Antalet provtillfällen är inte begränsat. Med prov " \
                                                               "jämställs också andra obligatoriska kursdelar. " \
                                                               "Studerande som godkänts på prov får inte genomgå " \
                                                               "förnyat prov för högre betyg. En student, " \
                                                               "som utan godkänt resultat har genomgått två prov för " \
                                                               "en kurs eller en del av en kurs, har rätt att få en " \
                                                               "annan examinator utsedd, om inte särskilda skäl talar " \
                                                               "mot det. Framställan härom ska göras till " \
                                                               "institutionsstyrelsen. Kursen har minst tre " \
                                                               "examinationstillfällen för varje del per läsår de år " \
                                                               "då undervisning ges. För de läsår som kursen inte ges " \
                                                               "erbjuds minst ett examinationstillfälle.<br><br>" \
                                                             + self.examination_f()

    def literature(self):
        if self.data["eligibility"] == "Självständigt arbete":
            self.texts["16. Kurslitteratur och övriga läromedel"] = "Litteraturen baseras på vetenskapliga " \
                                                                    "publikationer och rapporter inom det aktuella " \
                                                                    "området framtagna av den studerande genom " \
                                                                    "litteratursökning samt litteratur utdelad av " \
                                                                    "huvudhandledaren och/eller av den biträdande " \
                                                                    "handledaren.<br>"
        else:
            department = self.data["department"]
            self.texts[
                "16. Kurslitteratur och övriga läromedel"] = "Kurslitteratur beslutas av institutionsstyrelsen och " \
                                                             "publiceras på " + department + "s webbplats senast " \
                                                                                            "2 månader före kursstart.<br>"

    def transitions(self):
        self.texts["17. Övergångsbestämmelser"] = "Studerande kan begära att examination genomförs enligt denna " \
                                                  "kursplan även efter det att den upphört att gälla, dock högst tre " \
                                                  "gånger under en tvåårsperiod efter det att kursen har avvecklats. " \
                                                  "Framställan härom ska göras till institutionsstyrelsen. " \
                                                  "Bestämmelsen gäller även vid revidering av kursplanenochrevidering " \
                                                  "av kurslitteratur.<br>"

    def limitations(self):
        limitations_text = ""
        if self.data["forbidden_main"] != "":
            limitations_text += "Kursen kan ej ingå i examen inom huvudområdet " \
                                + self.data["forbidden_main"] + ".<br><br>"
        if self.data["forbidden_course"] != "":
            limitations_text += "Kursen kan ej ingå i examen tillsammans med kurserna " \
                                + self.data["forbidden_course"] + " eller motsvarande.<br>"
        self.texts["18. Begränsningar"] = limitations_text

    def other(self):
        other_text = ""
        if self.data["relations"] == "Fristående":
            other_text += "Kursen ges som fristående kurs."
        elif self.data["relations"] == "Ingår i program":
            other_text += "Kursen ingår i " + self.data["program"] + "."
        elif self.data["relations"] == "Program och fristående":
            other_text += "Kursen ingår i " + self.data["program"] + ", men kan också läsas som fristående kurs."
        self.texts["19. Övrigt"] = other_text

    def save_texts(self):
        self.eligibility()
        self.course_desc()
        self.expected_results()
        self.teaching()
        self.examination()
        self.literature()
        self.transitions()
        self.limitations()
        self.other()
        # with open("course_texts.json", "w", encoding="utf-8") as data:
        #     json.dump(self.texts, data, indent=4, ensure_ascii=False)

    def human_readable(self):
        self.save_texts()
        text_file = open("hr_texts.html", "w")
        for title, text in self.texts.items():
            text_file.write("<h3>" + title + "</h3>" + text)
        text_file.close()