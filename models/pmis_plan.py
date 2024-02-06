# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.exceptions import ValidationError


class PmisProjectPlanTemplate(models.Model):
    _name = "pmis.plan.template"
    _description = "Plan"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'category_id'

    procurement_directorate = fields.Char(string='Procurement Directorate', required=True,
                                          default="Ministry of Communicaton & Information Technology")
    financial_year = fields.Integer(string='Financial Year',
                                    limit=4,
                                    default=date.today().year
                                    )

    project_plan_ids = fields.One2many(
        comodel_name="pmis.project.plan",
        inverse_name="plan_template_id",
        readonly=False,
        copy=True,
        tracking=True,
    )

    @api.onchange('project_plan_ids')
    def onchange_project_plan_ids(self):
        for rec in self.project_plan_ids:
            if rec.project_eligibility_evaluation_date and rec.procurement_process_start_date:
                if rec.project_eligibility_evaluation_date < rec.procurement_process_start_date:
                    raise ValidationError(_("Project Eligibility Date not be before project start date"))
            if rec.project_announcement_date and rec.project_eligibility_evaluation_date:
                if rec.project_announcement_date < rec.project_eligibility_evaluation_date:
                    raise ValidationError(_("Project Announcement Date can't be before project Eligibility date"))
            if rec.project_offer_opening_date and rec.project_announcement_date:
                if rec.project_offer_opening_date < rec.project_announcement_date:
                    raise ValidationError(_("Project Offer Opening Date can't be before project Announcement date"))
            if rec.project_offer_evaluation_last_date and rec.project_offer_opening_date:
                if rec.project_offer_evaluation_last_date < rec.project_offer_opening_date:
                    raise ValidationError(_("Project Offer Evaluation Date can't be before project Offer opening date"))
            if rec.project_reporting_date and rec.project_offer_evaluation_last_date:
                if rec.project_reporting_date < rec.project_offer_evaluation_last_date:
                    raise ValidationError(
                        _("Project Offer Evaluation Report Date can't be before project Offer Evaluation date"))
            if rec.project_award_date and rec.project_reporting_date:
                if rec.project_award_date < rec.project_reporting_date:
                    raise ValidationError(_("Project award Date can't be before project report date"))
            if rec.project_commission_date and rec.project_award_date:
                if rec.project_commission_date < rec.project_award_date:
                    raise ValidationError(_("Project Commission Date can't be before Award date"))
            if rec.contract_sign_date and rec.project_commission_date:
                if rec.contract_sign_date < rec.project_commission_date:
                    raise ValidationError(_("Project Contract sign Date can't be before commission date"))
            if rec.project_end_date and rec.contract_sign_date:
                if rec.project_end_date < rec.contract_sign_date:
                    raise ValidationError(_("Project End Date can't be before contract signing date"))
            if rec.project_technical_documents_date and rec.project_end_date:
                if rec.project_technical_documents_date < rec.project_end_date:
                    raise ValidationError(
                        _("Project Technical Document submission Date can't be before project end date"))

    tadel_id = fields.Many2one(
        comodel_name="pmis.plan.tadel",
        string="Tadel",
        readonly=False,
        copy=True,
        tracking=True,

    )
    category_id = fields.Many2one(
        comodel_name='pmis.procurement.category',
        string="Procurement Type", required=True,
    )

    @api.model
    def create(self, vals):
        if self.env['pmis.plan.template'].search(
                [('financial_year', '=', vals.get('financial_year')), ('category_id', '=', vals.get('category_id'))]):
            raise ValidationError(_("You can create only one plan every year"))
        return super(PmisProjectPlanTemplate, self).create(vals)

    def unlink(self):
        if self.project_plan_ids:
            for rec in self.project_plan_ids:
                self.env['pmis.project'].browse(rec.project_id.id).write({'state': 'draft'})
        return super(PmisProjectPlanTemplate, self).unlink()


class PmisProjectPlan(models.Model):
    _name = "pmis.project.plan"
    _description = "Plan"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'project_id'

    sector = fields.Selection([('resource', 'Resource'), ('developing', 'Developing'), ], string='Sector')

    def get_sector_label(self):
        label_mapping = {
            'resource': 'Resource',
            'developing': 'Developing',
        }
        return label_mapping.get(self.sector, '')

    procurement_directorate = fields.Selection([('mcit', 'MCIT')], string='MCIT')
    budget_type = fields.Selection([('normal', 'Normal'), ('developing', 'Developing'), ], string='Budget Type')
    budget_type_is_optional = fields.Selection([('optional', 'Optional'), ('not_optional', 'Not Optional'), ],
                                               string='Optional Budget', default='optional')
    project_description = fields.Text(string='Description')
    planned_project_type = fields.Selection([('new', 'New'), ('transferred', 'Developing'), ], string='Project Type')
    inner_resource_preferred = fields.Selection([('1', 'Yes'), ('0', 'No'), ], string='Inner Resource Preferred')
    budget_amount = fields.Float(string='Project Amount')
    project_start_date = fields.Date(string='Start Date', )
    project_eligibility_evaluation_date = fields.Date(string='Eligibility Evaluation')
    project_announcement_date = fields.Date(string='Announcement Date')
    project_offer_opening_date = fields.Date(string='Offer Opening')
    project_offer_evaluation_last_date = fields.Date(string='Offer Evaluation')
    project_reporting_date = fields.Date(string='Reporting Date')
    project_award_date = fields.Date(string='Award Date')
    project_commission_date = fields.Date(string='Commission Date')
    project_duration = fields.Integer(string='Duration')
    project_end_date = fields.Date(string='End Date')
    project_technical_documents_date = fields.Date(string='Technical Documents Completion Date')
    contract_sign_date = fields.Date(string='Contract Sign Date')
    procurement_process_start_date = fields.Date(string='Procurement Process Start Date')
    contract_type = fields.Selection([
        ('sum_lum', 'Contract Sum Lum'),
        ('unit_price', 'Contract Unit Price'),
        ('framework', 'Framework'),
        ('percentage', 'Contract Base Percentage'),
        ('supply_chain', ' Erection and  Supply, Design for Contract'),
        ('industrial', 'Plant Industrial For Contract Turnke'),
        ('build_design', 'Contracts Build & Design'),
        ('pos_payment', 'Post Payment'),
        ('other', 'Other')
    ],
        string='Contract Type',
        default='sum_lum'
    )
    # contract_number = fields.Char(string='Contract Number', related='project_id.project_number')
    contract_number = fields.Char(string='Contract Number')
    procurement_rawish = fields.Selection([
        ('ncb', 'NCB'),
        ('icb', 'ICB'),
        ('other', 'Other'),
    ],
        string='Procurement Rawish',
        default='ncb'
    )
    procurement_rawish_other = fields.Text(string='Procurement New Rawish')

    project_id = fields.Many2one(
        comodel_name="pmis.project",
        string="Project",
        readonly=False,
        tracking=True,
        ondelete='restrict',
    )
    # ondelete = 'cascade' ondelete='restrict'
    project_name_en = fields.Char(string='Project Name', related='project_id.name')

    # consultative project
    estimated_cost = fields.Char(related='project_id.estimated_cost')
    cons_interested_announcement_date = fields.Date(string='Interesting Date')
    cons_shortlist_date = fields.Date(string='Short list Date')
    cons_offer_submission_date = fields.Date(string='Offer Submission')
    cons_technical_offer_opening_date = fields.Date(string='Technical Offer Opening')
    cons_offer_evaluation_report_sign_date = fields.Date(string='Offer Evaluation Report Sign Date')
    cons_mess_evaluation_report_sign_date = fields.Date(string='Offer Mess Evaluation Report Sign Date')
    cons_financial_offer_opening_date = fields.Date(string='Financial Offer Opening')
    cons_negotiation_end_date = fields.Date(string='Negotiation End Date')

    donor_id = fields.Many2one(
        comodel_name="pmis.project.donor",
        string="Donor",
        readonly=False,
        tracking=True,
    )

    project_state = fields.Selection(
        related="project_id.state",
        string='State')

    plan_template_id = fields.Many2one(
        comodel_name="pmis.plan.template",
        string="Plan",
        readonly=False,
        copy=True,
        tracking=True,
    )

    category_id = fields.Many2one(
        comodel_name='pmis.procurement.category',
        string="Procurement Type", required=True,
        related='plan_template_id.category_id'
    )
    province = fields.Many2one('pmis.country.province', string='Province')
    district = fields.Many2one('pmis.districts', string='District', domain="[('id', 'in', avialable_district_ids)]")

    avialable_district_ids = fields.Many2many('pmis.districts', compute = '_compute_avialable_district')

    @api.depends('province')
    def _compute_avialable_district(self):
        for rec in self:
            rec.avialable_district_ids = rec.province.district_ids


    # district = fields.Selection([
    #     ('ustalaf', 'Ustalaf'),
    #     ('bagrami', 'Bagrami'),
    #     ('paghman', 'Paghman'),
    #     ('chahar_asiab', 'Chahar Asiab'),
    #     ('khak_jabar', 'Khak Jabar'),
    #     ('deh_sabz', 'Deh Sabz'),
    #     ('sarobi', 'Sarobi'),
    #     ('shakar_dara', 'Shakar Dara'),
    #     ('farza', 'Farza'),
    #     ('qara_bagh', 'Qara Bagh'),
    #     ('kabul', 'Kabul (Capital)'),
    #     ('kalkan', 'Kalkan'),
    #     ('gul_dara', 'Gul Dara'),
    #     ('mosai', 'Mosai'),
    #     ('mer_bacha_kot', 'Mer Bacha Kot'),
    #     ('chora', 'Chora'),
    #     ('dehrawad', 'Dehrawad'),
    #     ('gizab', 'Gizab'),
    #     ('khas_urzgan', 'Khas Urzgan'),
    #     ('shahide_hasas', 'Shahide Hasas'),
    #     ('trinkot', 'Trinkot'),
    #     ('qale_now', 'Qale-now'),
    #     ('abkamre', 'Abkamre'),
    #     ('jond', 'Jond'),
    #     ('ghormach', 'Ghormach'),
    #     ('maqar', 'Maqar'),
    #     ('qadis', 'Qadis'),
    #     ('bala_marghab', 'Bala Marghab'),
    #     ('shebar', 'Shebar'),
    #     ('yakawang', 'Yakawang'),
    #     ('sighan', 'Sighan'),
    #     ('panjan', 'Panjan'),
    #     ('was', 'Was'),
    #     ('kahmard', 'Kahmard'),
    #     ('arghanjawa', 'Arghanjawa'),
    #     ('argo', 'Argo'),
    #     ('ashkasham', 'Ashkasham'),
    #     ('baharak', 'Baharak'),
    #     ('tabshakan', 'Tabshakan'),
    #     ('joram', 'Joram'),
    #     ('khash', 'Khash'),
    #     ('khawahan', 'Khawahan'),
    #     ('darim', 'Darim'),
    #     ('darwaz_bala', 'Darwaz Bala'),
    #     ('drwaz', 'Drwaz'),
    #     ('ragh', 'Ragh'),
    #     ('zibak', 'Zibak'),
    #     ('shaghnan', 'Shaghnan'),
    #     ('shahr_bazark', 'Shahr Bazark'),
    #     ('shabki', 'Shabki'),
    #     ('faiz_abad', 'Faiz Abad'),
    #     ('kasham', 'Kasham'),
    #     ('koran_wa_menjan', 'Koran wa Menjan'),
    #     ('kof_ab', 'Kof Ab'),
    #     ('kohistan', 'Kohistan'),
    #     ('wakhan', 'Wakhan'),
    #     ('wardaj', 'Wardaj'),
    #     ('yawan', 'Yawan'),
    #     ('yaftal_safla', 'Yaftal Safla'),
    #     ('yamgan', 'Yamgan'),
    #     ('andrab', 'Andrab'),
    #     ('barka', 'Barka'),
    #     ('pul_hisar', 'Pul Hisar'),
    #     ('pul_khumre', 'Pul Khumre'),
    #     ('tala_wa_barfak', 'Tala wa Barfak'),
    #     ('khanjan', 'Khanjan'),
    #     ('khawaja_hijran', 'Khawaja Hijran'),
    #     ('khost_wa_farang', 'Khost wa Farang'),
    #     ('dah_salih', 'Dah Salih'),
    #     ('dahna_ghore', 'Dahna Ghore'),
    #     ('dushe', 'Dushe'),
    #     ('frang_wa_gharo', 'Frang wa Gharo'),
    #     ('guzar_ga', 'Guzar Ga'),
    #     ('nahrin', 'Nahrin'),
    #     ('nawe_baghlan', 'Nawe Baghlan'),
    #     ('char_bolak', 'Char Bolak'),
    #     ('charakment', 'Charakment'),
    #     ('chamtal', 'Chamtal'),
    #     ('dawlat_abad', 'Dawlat Abad'),
    #     ('da_dade', 'Da Dade'),
    #     ('kaldar', 'Kaldar'),
    #     ('kholam', 'Kholam'),
    #     ('kashanda', 'Kashanda'),
    #     ('marmal', 'Marmal'),
    #     ('nehr_shahi', 'Nehr Shahi'),
    #     ('sholgara', 'Sholgara'),
    #     ('shortipa', 'Shortipa'),
    #     ('zari', 'Zari'),
    #     ('charekar', 'Charekar'),
    #     ('bagrami', 'Bagrami'),
    #     ('ghor_bank', 'Ghor Bank'),
    #     ('jabal_siraj', 'Jabal Siraj'),
    #     ('koh_safi', 'Koh Safi'),
    #     ('salang', 'Salang'),
    #     ('said_khil', 'Said Khil'),
    #     ('shekh_ali', 'Shekh Ali'),
    #     ('shinwari', 'Shinwari'),
    #     ('surkh_parsa', 'Surkh Parsa'),
    #     ('ahmad_abad', 'Ahmad Abad'),
    #     ('zazi', 'Zazi'),
    #     ('zurmat', 'Zurmat'),
    #     ('jan_khil', 'Jan Khil'),
    #     ('chawak', 'Chawak'),
    #     ('samkani', 'Samkani'),
    #     ('dand_patan', 'Dand Patan'),
    #     ('said_karam', 'Said Karam'),
    #     ('shwak', 'Shwak'),
    #     ('ali_khil', 'Ali Khil'),
    #     ('garda', 'Garda'),
    #     ('ghardiz', 'Ghardiz'),
    #     ('ahmad_khil', 'Ahmad Khil'),
    #     ('merzka', 'Merzka'),
    #     ('laja', 'LaJa'),
    #     ('zurmat', 'Zurmat'),
    #     ('barmal', 'Barmal'),
    #     ('dela', 'Dela'),
    #     ('gian', 'Gian'),
    #     ('gomal', 'Gomal'),
    #     ('jane_khil', 'Jane khil'),
    #     ('mata', 'Mata'),
    #     ('nika', 'Nika'),
    #     ('omna', 'Omna'),
    #     ('sar_hawza', 'Sar Hawza'),
    #     ('terwa', 'Terwa'),
    #     ('orgon', 'Orgon'),
    #     ('waza_khwa', 'Waza Khwa'),
    #     ('warmame', 'Warmame'),
    #     ('yahya_khil', 'Yahya khil'),
    #     ('yousuf_khil', 'Yousuf Khil'),
    #     ('zarghon', 'Zarghon'),
    #     ('zerok', 'Zerok'),
    #     ('anaba', 'Anaba'),
    #     ('bazarak', 'Bazarak'),
    #     ('paryan', 'Paryan'),
    #     ('khanj', 'Khanj'),
    #     ('dara', 'Dara'),
    #     ('rokha', 'Rokha'),
    #     ('shawtal', 'Shawtal'),
    #     ('talqan', 'Talqan'),
    #     ('rustaq', 'Rustaq'),
    #     ('khawaja_ghar', 'Khawaja Ghar'),
    #     ('ashkasham', 'Ashkasham'),
    #     ('bangi', 'Bangi'),
    #     ('chal', 'Chal'),
    #     ('chah_ab', 'Chah Ab'),
    #     ('yangi_kala', 'Yangi Kala'),
    #     ('darqad', 'Darqad'),
    #     ('farkhar', 'Farkhar'),
    #     ('klafgan', 'Klafgan'),
    #     ('baharak', 'Baharak'),
    #     ('khwaja_bahaoudin', 'Khwaja Bahaoudin'),
    #     ('dasht_qala', 'Dasht Qala'),
    #     ('namak_ab', 'Namak Ab'),
    #     ('warsaj', 'Warsaj'),
    #     ('hazar_samoch', 'Hazar Samoch'),
    #     ('aqcha', 'Aqcha'),
    #     ('darzab', 'Darzab'),
    #     ('faiz_abad', 'Faiz abad'),
    #     ('khamab', 'Khamab'),
    #     ('khanqa', 'Khanqa'),
    #     ('khwaja_do_koh', 'Khwaja Do Koh'),
    #     ('mardoina', 'Mardoina'),
    #     ('metgajek', 'Metgajek'),
    #     ('qarqin', 'Qarqin'),
    #     ('daqash', 'Dqash'),
    #     ('shabr_ghan', 'Shabr Ghan'),
    #     ('bak', 'Bak'),
    #     ('gurbaz', 'Gurbaz'),
    #     ('zazi_midan', 'Zazi Midan'),
    #     ('maton', 'Maton'),
    #     ('ismail_khil', 'Ismail Khil'),
    #     ('mosa_khil', 'Mosa Khil'),
    #     ('nadarsh_kot', 'Nadarsh Kot'),
    #     ('qalandar', 'Qalandar'),
    #     ('sabre', 'Sabre'),
    #     ('shamal', 'Shamal'),
    #     ('spera', 'Spera'),
    #     ('tani', 'Tani'),
    #     ('terezabi', 'Terezabi'),
    #     ('mangal', 'Mangal'),
    #     ('neli', 'Neli'),
    #     ('ashtarli', 'Ashtarli'),
    #     ('khader', 'Khader'),
    #     ('sang_takht', 'Sang Takht'),
    #     ('sharistan', 'Sharistan'),
    #     ('kujran', 'Kujran'),
    #     ('gezab', 'Gezab'),
    #     ('shajoe', 'Shajoe'),
    #     ('shahr_safa', 'Shahr Safa'),
    #     ('mezana', 'Mezana'),
    #     ('daya_chopan', 'Daya Chopan'),
    #     ('khak_afghan', 'Khak Afghan'),
    #     ('arghandab', 'Arghandab'),
    #     ('shore', 'Shore'),
    #     ('shikai', 'Shikai'),
    #     ('nobahar', 'Nobahar'),
    #     ('shamlzai', 'Shamlzai'),
    #     ('atghar', 'Atghar'),
    #     ('balkhab', 'Balkhab'),
    #     ('gosfandari', 'Gosfandari'),
    #     ('kohistanat', 'Kohistanat'),
    #     ('sang_cahrk', 'Sang Cahrk'),
    #     ('sre_pul', 'Sre Pul'),
    #     ('sayad', 'Sayad'),
    #     ('sozma_kala', 'Sozma Kala'),
    #     ('aibak', 'Aibak'),
    #     ('dara_sawfi', 'Dara Sawfi'),
    #     ('hazrat_sultan', 'Hazrat Sultan'),
    #     ('khrm_sarbagh', 'Khrm Sarbagh'),
    #     ('roe_do_ab', 'Roe Do Ab'),
    #     ('andar', 'Andar'),
    #     ('da_yak', 'Da Yak'),
    #     ('ghaghto', 'Ghaghto'),
    #     ('khogani', 'Khogani'),
    #     ('dwaghiz', 'Dwaghiz'),
    #     ('gero', 'Gero'),
    #     ('qara_bagh', 'Qara Bagh'),
    #     ('maqar', 'Maqar'),
    #     ('jahgori', 'Jahgori'),
    #     ('ajristan', 'Ajristan'),
    #     ('navi', 'Navi'),
    #     ('zankhan', 'Zankhan'),
    #     ('gelan', 'Gelan'),
    #     ('feroz_koh', 'Feroz Koh'),
    #     ('yaspaband', 'Yaspaband'),
    #     ('dah_marghab', 'Dah Marghab'),
    #     ('tolak', 'Tolak'),
    #     ('tayora', 'Tayora'),
    #     ('saghir', 'Saghir'),
    #     ('dawlat', 'Dawlat'),
    #     ('charsada', 'Charsada'),
    #     ('shahrk', 'Shahrk'),
    #     ('lal_wa_sarjangan', 'Lal wa Sarjangan'),
    #     ('almar', 'Almar'),
    #     ('belchrigh', 'Belchrigh'),
    #     ('and_khoi', 'And Khoi'),
    #     ('pakhton', 'Pakhton'),
    #     ('khana_cahar_bagh', 'Khana Cahar Bagh'),
    #     ('dawlat_abad', 'Dawlat Abad'),
    #     ('khwaja_sabz', 'Khwaja Sabz'),
    #     ('sherin_tagab', 'Sherin Tagab'),
    #     ('qarghan', 'Qarghan'),
    #     ('qarmgul', 'Qarmgul'),
    #     ('qisar', 'Qisar'),
    #     ('kohistan', 'Kohistan'),
    #     ('garziwan', 'Garziwan'),
    #     ('memnana', 'Memnana'),
    #     ('anar', 'Anar'),
    #     ('bala_balok', 'Bala Balok'),
    #     ('parchaman', 'Parchaman'),
    #     ('bakwa', 'Bakwa'),
    #     ('pusht_rod', 'Pusht rod'),
    #     ('khak_safid', 'Khak Safid'),
    #     ('shaib_ko', 'Shaib Ko'),
    #     ('farah', 'Farah'),
    #     ('qala_kawa', 'Qala Kawa'),
    #     ('gulistan', 'Gulistan'),
    #     ('lash_wa_jawain', 'Lash wa Jawain'),
    #     ('alasai', 'Alasai'),
    #     ('hisa_1_kohistan', 'Hisa 1 Kohistan'),
    #     ('hisa_2_kohistan', 'Hisa 2 Kohistan'),
    #     ('koh_bank', 'Koh Bank'),
    #     ('mahmod_raqi', 'Mahmod Raqi'),
    #     ('nijrab', 'Nijrab'),
    #     ('tagab', 'Tagab'),
    #     ('ali_abad', 'Ali Abad'),
    #     ('arche', 'Arche'),
    #     ('chadara', 'Chadara'),
    #     ('aimam_saib', 'Aimam Saib'),
    #     ('khan_abad', 'Khan Abad'),
    #     ('kunduz', 'Kunduz'),
    #     ('qalazal', 'Qalazal'),
    #     ('daman', 'Daman'),
    #     ('sha_wali_kot', 'Sha Wali Kot'),
    #     ('arghandab', 'Arghandab'),
    #     ('ghorak', 'Ghorak'),
    #     ('miwand', 'Miwand'),
    #     ('panjwai', 'Panjwai'),
    #     ('rabak', 'Rabak'),
    #     ('shorabak', 'Shorabak'),
    #     ('spen_boldak', 'Spen Boldak'),
    #     ('arghistan', 'Arghistan'),
    #     ('marof', 'Marof'),
    #     ('khakriz', 'Khakriz'),
    #     ('dand', 'Dand'),
    #     ('nekh', 'Nekh'),
    #     ('zerai', 'Zerai'),
    #     ('takhta_pul', 'Takhta Pul'),
    #     ('mianshin', 'Mianshin'),
    #     ('asadabad', 'Asadabad'),
    #     ('khas_kunar', 'Khas Kunar'),
    #     ('chapa_dara', 'Chapa Dara'),
    #     ('dangam', 'Dangam'),
    #     ('pech_dara', 'Pech Dara'),
    #     ('ghazi_abad', 'Ghazi Abad'),
    #     ('marawara', 'Marawara'),
    #     ('narang_wa_badil', 'Narang wa Badil'),
    #     ('narai', 'Narai'),
    #     ('norgal', 'Norgal'),
    #     ('sawkai', 'Sawkai'),
    #     ('sarkano', 'Sarkano'),
    #     ('wata_poor', 'Wata Poor'),
    #     ('alingar', 'Alingar'),
    #     ('alishang', 'Alishang'),
    #     ('qarghio', 'Qarghio'),
    #     ('dawalt_sha', 'Dawalt Sha'),
    #     ('mihtarlam', 'Mihtarlam'),
    #     ('sarkh', 'Sarkh'),
    #     ('kharwar', 'Kharwar'),
    #     ('barke_barak', 'Barke Barak'),
    #     ('khokhai', 'Khokhai'),
    #     ('azra', 'Azra'),
    #     ('haska_mina', 'Haska Mina'),
    #     ('achin', 'Achin'),
    #     ('bahsood', 'Bahsood'),
    #     ('chaprhar', 'Chaprhar'),
    #     ('dare_nor', 'Dare nor'),
    #     ('batekot', 'Batekot'),
    #     ('dur_baba', 'Dur Baba'),
    #     ('goshta', 'Goshta'),
    #     ('hisarak', 'Hisarak'),
    #     ('jala_kot', 'Jala Kot'),
    #     ('kama', 'Kama'),
    #     ('khogani', 'Khogani'),
    #     ('khiwa', 'Khiwa'),
    #     ('lalpora', 'Lalpora'),
    #     ('momandara', 'Momandara'),
    #     ('nazian', 'Nazian'),
    #     ('pachiragam', 'Pachiragam'),
    #     ('rodat', 'Rodat'),
    #     ('sherzad', 'Sherzad'),
    #     ('ghani_khil', 'Ghani Khil'),
    #     ('spin_ghar', 'Spin Ghar'),
    #     ('sara_rod', 'Sara Rod'),
    #     ('bargmatal', 'Bargmatal'),
    #     ('do_ab', 'Do Ab'),
    #     ('kamdish', 'Kamdish'),
    #     ('norgram', 'Norgram'),
    #     ('mandol', 'Mandol'),
    #     ('paron', 'Paron'),
    #     ('wama', 'Wama'),
    #     ('waigal', 'Waigal'),
    #     ('zranj', 'Zranj'),
    #     ('chakhansor', 'Chakhansor'),
    #     ('char_barjak', 'Char Barjak'),
    #     ('kang', 'Kang'),
    #     ('khash_road', 'Khash Road'),
    #     ('dilaram', 'Dilaram'),
    #     ('midan', 'Midan'),
    #     ('chack', 'Chack'),
    #     ('said_abad', 'Said Abad'),
    #     ('daimerdad', 'Daimerdad'),
    #     ('jaghato', 'Jaghato'),
    #     ('narkh', 'Narkh'),
    #     ('jaliz', 'Jaliz'),
    #     ('behsood_awal', 'Behsood Awal'),
    #     ('behsood_dum', 'Behsood Dum'),
    #     ('hirat', 'Hirat'),
    #     ('anjil', 'Anjil'),
    #     ('pakhtoon', 'Pakhtoon'),
    #     ('guzra', 'Guzra'),
    #     ('kharkh', 'Kharkh'),
    #     ('kashk', 'Kashk'),
    #     ('gulran', 'Gulran'),
    #     ('kohistan', 'Kohistan'),
    #     ('ghoryan', 'Ghoryan'),
    #     ('zinda_jan', 'Zinda Jan'),
    #     ('adrskan', 'Adrskan'),
    #     ('shin_dand', 'Shin Dand'),
    #     ('obe', 'Obe'),
    #     ('farsi', 'Farsi'),
    #     ('chast_sharif', 'Chast Sharif'),
    #     ('lashkarga', 'Lashkarga'),
    #     ('kajake', 'Kajake'),
    #     ('nahr_siraj', 'Nahr Siraj'),
    #     ('mosa_kala', 'Mosa Kala'),
    #     ('baghran', 'Baghran'),
    #     ('nawzad', 'Nawzad'),
    #     ('washir', 'Washir'),
    #     ('nadali', 'Nadali'),
    #     ('nawa', 'Nawa'),
    #     ('khanshin', 'Khanshin'),
    #     ('disho', 'Disho'),
    #     ('garmsir', 'Garmsir'),
    #     ('sarwan_kala', 'Sarwan Kala'),
    #
    # ], string="District", required=True)
    #
    # province = fields.Selection([
    #     ('Badakhshan', 'Badakhshan'),
    #     ('Badghis', 'Badghis'),
    #     ('Baghlan', 'Baghlan'),
    #     ('Balkh', 'Balkh'),
    #     ('Bamyan', 'Bamyan'),
    #     ('Daykundi', 'Daykundi'),
    #     ('Farah', 'Farah'),
    #     ('Faryab', 'Faryab'),
    #     ('Ghazni', 'Ghazni'),
    #     ('Ghor', 'Ghor'),
    #     ('Helmand', 'Helmand'),
    #     ('Herat', 'Herat'),
    #     ('Jowzjan', 'Jowzjan'),
    #     ('Kabul', 'Kabul'),
    #     ('Kandahar', 'Kandahar'),
    #     ('Kapisa', 'Kapisa'),
    #     ('Khost', 'Khost'),
    #     ('Kunar', 'Kunar'),
    #     ('Kunduz', 'Kunduz'),
    #     ('Laghman', 'Laghman'),
    #     ('Logar', 'Logar'),
    #     ('Nangarhar', 'Nangarhar'),
    #     ('Nimroz', 'Nimroz'),
    #     ('Nuristan', 'Nuristan'),
    #     ('Paktia', 'Paktia'),
    #     ('Paktika', 'Paktika'),
    #     ('Panjshir', 'Panjshir'),
    #     ('Parwan', 'Parwan'),
    #     ('Samangan', 'Samangan'),
    #     ('Sar-e Pol', 'Sar-e Pol'),
    #     ('Takhar', 'Takhar'),
    #     ('Urozgan', 'Urozgan'),
    #     ('Wardak', 'Wardak'),
    #     ('Zabul', 'Zabul'),
    # ], string="Province", required=True)

    village = fields.Char(string='Village')

    @api.model
    def default_get(self, fields):
        res = super(PmisProjectPlan, self).default_get(fields)
        return res

    # update state in project model
    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_id']).write({'state': 'plan'})
        return super(PmisProjectPlan, self).create(vals)

    def write(self, vals):
        return super(PmisProjectPlan, self).write(vals)

    def unlink(self):
        for rec in self:
            self.env['pmis.project'].browse(rec.project_id.id).write({'state': 'draft'})
        return super(PmisProjectPlan, self).unlink()


class PmisProjectDonor(models.Model):
    _name = "pmis.project.donor"
    _description = "Project Donor"
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)


class PmisPlanTadel(models.Model):
    _name = "pmis.plan.tadel"
    _description = "Plan Tadel"
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)

    plan_template_ids = fields.One2many(
        comodel_name="pmis.plan.template",
        inverse_name="tadel_id",
        string="Projects",
        readonly=False,
        copy=True,
        tracking=True,
    )
