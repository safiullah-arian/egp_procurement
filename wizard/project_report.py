from odoo import api, fields, models, _, tools
from datetime import datetime, date


class PmisPlanReport(models.TransientModel):
    _name = "pmis.project.pdf.report"
    _description = "PMIS Plan Report"

    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('plan', 'Plan'),
    #     ('announce', 'Announced'),
    #     ('received_offers', 'Offer Receiving'),
    #     ('offer_opening', 'Opening Offers'),
    #     ('offer_details', 'Offer Details'),
    #     ('offer_testing', 'Offer Testing'),
    #     ('offer_evaluation', 'Offer Evaluation'),
    #     ('offer_winning', 'Offer Winner'),
    #     ('won', 'Winner'),
    #     ('appeal', 'Appeal'),
    #     ('contract', 'Award'),
    #     ('delivery', 'Delivery'),
    #     ('payment', 'Payment'),
    #     ('cancel', 'Cancel'),
    #     ('shortlist', 'Shortlist'),
    #     ('consult_offers_received', 'Offer Receiving'),
    #     ('consult_offersghoshai', 'Offer Ghoshai'),
    #     ('consult_evaluation', 'Offer Evaluation'),
    #     ('consult_interview', 'Interview'),
    #     ('consult_winners', 'Winners'),
    #     ('consult_candidate_won', 'Winner Candidates'),
    # ],
    #     string='States', default='', )

    report_from = fields.Date(string='Report From')
    report_up_to = fields.Date(string='Report To')

    category_id = fields.Many2one(
        comodel_name='pmis.procurement.category',
        string="Procurement Type")

    cat_id = fields.Integer(string='id')

    @api.onchange('category_id')
    def onchange_category_id(self):
        self.cat_id = self.category_id.id

    def action_print_report(self):
        data = {
            # 'state': self.state,
            'report_from': self.report_from,
            'report_up_to': self.report_up_to,
            'category_id': self.category_id.id,
            'cat_id': self.cat_id,
        }
        return self.env.ref('egp_procurement.action_pmis_projects_report').report_action(self, data=data)


class PmisPlanReportAbstract(models.AbstractModel):
    _name = "report.egp_procurement.projects_report_template"
    _description = "PMIS Projects Report"

    def _get_report_values(self, docids, data=None):

        draft_domain = []
        plan_domain = []
        announce_domain = []
        offer_receiving_domain = []
        offer_opening_domain = []
        offer_details_domain = []
        offer_evaluation_domain = []
        candidate_winning_domain = []
        contract_decision = []
        contract_management_domain = []
        delivery_description_domain = []
        payment_domain = []

        docs = self.env['pmis.project'].search([('category_id', '=', data.get('category_id'))])


        if data.get('report_from'):
            draft_domain.append(('date_recieved', '>=', data.get('report_from')))
            plan_domain.append(('create_date', '>=', data.get('report_from')))
            announce_domain.append(('pro_announcement_date', '>=', data.get('report_from')))
            offer_receiving_domain.append(('create_date', '>=', data.get('report_from')))
            offer_opening_domain.append(('offer_ghoshai_date', '>=', data.get('report_from')))
            offer_details_domain.append(('create_date', '>=', data.get('report_from')))
            offer_evaluation_domain.append(('create_date', '>=', data.get('report_from')))
            candidate_winning_domain.append(('create_date', '>=', data.get('report_from')))
            contract_decision.append(('create_date', '>=', data.get('report_from')))
            contract_management_domain.append(('create_date', '>=', data.get('report_from')))
            delivery_description_domain.append(('delivery_date', '>=', data.get('report_from')))
            payment_domain.append(('create_date', '>=', data.get('report_from')))

        if data.get('report_up_to'):
            draft_domain.append(('date_recieved', '<=', data.get('report_up_to')))
            plan_domain.append(('create_date', '<=', data.get('report_up_to')))
            announce_domain.append(('pro_announcement_end_date', '<=', data.get('report_up_to')))
            offer_receiving_domain.append(('create_date', '<=', data.get('report_up_to')))
            offer_opening_domain.append(('offer_ghoshai_date', '<=', data.get('report_up_to')))
            offer_details_domain.append(('create_date', '<=', data.get('report_up_to')))
            offer_evaluation_domain.append(('create_date', '<=', data.get('report_up_to')))
            candidate_winning_domain.append(('create_date', '<=', data.get('report_up_to')))
            contract_decision.append(('create_date', '<=', data.get('report_up_to')))
            contract_management_domain.append(('create_date', '<=', data.get('report_up_to')))
            delivery_description_domain.append(('delivery_date', '<=', data.get('report_up_to')))
            payment_domain.append(('create_date', '<=', data.get('report_up_to')))

        if data.get('category_id'):
            draft_domain.append((
                'category_id',
                '=', data.get('category_id')))

            plan_domain.append(('category_id', '=', data.get('category_id')))
            announce_domain.append(('planned_project_id.project_id.category_id', '=', data.get('category_id')))
            offer_receiving_domain.append(
                ('announced_project_id.planned_project_id.project_id.category_id', '=', data.get('category_id')))
            offer_opening_domain.append(('category_id', '=', data.get('category_id')))
            offer_details_domain.append((
                'offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id',
                '=', data.get('category_id')))
            offer_evaluation_domain.append((
                'offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id',
                '=', data.get('category_id')))
            candidate_winning_domain.append((
                'evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id',
                '=', data.get('category_id')))

            contract_decision.append((
                'evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id',
                '=', data.get('category_id')))
            contract_management_domain.append((
                'winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id',
                '=', data.get('category_id')))
            delivery_description_domain.append((
                'contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id',
                '=', data.get('category_id')))

            payment_domain.append((
                'delivery_project_id.contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id',
                '=', data.get('category_id')))

        plan_domain.append(('project_id.state', '=', 'plan'))
        announce_domain.append(('planned_project_id.project_id.state', '=', 'announce'))
        offer_receiving_domain.append(
            ('announced_project_id.planned_project_id.project_id.state', '=', 'received_offers'))
        offer_opening_domain.append((
            'offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
            '=', 'offer_opening'))
        offer_details_domain.append((
            'offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
            '=', 'offer_details'))

        offer_evaluation_domain.append((
            'offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
            '=', 'offer_testing'))

        candidate_winning_domain.append((
            'evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
            '=', 'winner_announcement'))

        contract_decision.append((
            'evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
            '=', 'offer_winning'))

        contract_management_domain.append((
            'winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
            '=', 'contract'))

        delivery_description_domain.append((
            'contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
            '=', 'delivery'))

        payment_domain.append((
            'delivery_project_id.contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
            '=', 'payment'))

        draft_domain.append((
            'state',
            '=', 'draft'))
        category_name = self.env['pmis.procurement.category'].browse(data.get('category_id')).name
        # projects
        draft_projects = self.env['pmis.project'].search(draft_domain)
        plan_projects = self.env['pmis.project.plan'].search(plan_domain)
        announced_projects = self.env['project.announcement'].search(announce_domain)
        offer_receiving_projects = self.env['pmis.offer_submission_project'].search(offer_receiving_domain)
        offer_opening_projects = self.env['pmis.offerghoshai'].search(offer_opening_domain)
        offer_details_projects = self.env['pmis.offers.details'].search(offer_details_domain)
        offer_evaluation_projects = self.env['pmis.offers.evaluation'].search(offer_evaluation_domain)

        candidate_winning_projects = self.env['pmis.bidding.winning.announcement'].search(candidate_winning_domain)

        contract_decision_projects = self.env['bidding.winner'].search(contract_decision)
        contract_management_projects = self.env['pmis.contract.management'].search(contract_management_domain)
        delivery_description_projects = self.env['pmis.delivery.description'].search(delivery_description_domain)
        payment_projects = self.env['pmis.payment'].search(payment_domain)

        print("draft_projects  ", draft_projects)
        print("plan", plan_projects)
        print("announced Projects", announced_projects)
        print("offer reciving Projects", offer_receiving_projects)
        print("opening Projects", offer_opening_projects)
        print("details Projects", offer_details_projects)
        print("evaluation Projects", offer_evaluation_projects)

        print("candidate_winning_projects", candidate_winning_projects)

        print("contract descision Projects", contract_decision_projects)
        print("contract  Projects", contract_management_projects)
        print("delivery_description_projects  ", delivery_description_projects)
        print("payment_projects  ", payment_projects)

        data.update(
            {
                'category_name': category_name,
                'draft_projects': draft_projects,
                'plan_projects': plan_projects,
                'announced_projects': announced_projects,
                'offer_receiving_projects': offer_receiving_projects,
                'offer_opening_projects': offer_opening_projects,
                'offer_details_projects': offer_details_projects,
                'offer_evaluation_projects': offer_evaluation_projects,
                'candidate_winning_projects': candidate_winning_projects,
                'contract_decision_projects': contract_decision_projects,
                'contract_management_projects': contract_management_projects,
                'delivery_description_projects': delivery_description_projects,
                'payment_projects': payment_projects
            })

        return {
            'doc_ids': docs.ids,
            'doc_model': 'pmis.project',
            'docs': docs,
            'datas': data
        }
