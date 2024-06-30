from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=True)
    diagnostico = db.Column(db.String(128))
    cid = db.Column(db.String(10))

    def __repr__(self):
        return f'<Paciente {self.nome}>'

class ServicoEspecializado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'<ServicoEspecializado {self.nome}>'

class ServicoManejo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'<ServicoManejo {self.nome}>'

class Diagnostico(db.Model):
    cid = db.Column(db.String(10), primary_key=True)
    descricao = db.Column(db.String(128))
    servico_especializado_id = db.Column(db.Integer, db.ForeignKey('servico_especializado.id'))
    servico_manejo_ids = db.Column(db.String(64))  # Can be a comma-separated list of IDs
    incluir_no_algoritmo = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Diagnostico {self.cid}>'

class FluxoAtendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    diagnostico_cid = db.Column(db.String(10), db.ForeignKey('diagnostico.cid'))
    etapa = db.Column(db.String(64))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    proximo_passo = db.Column(db.String(128))

    def __repr__(self):
        return f'<FluxoAtendimento {self.id}>'

@app.route('/')
def index():
    diagnosticos = Diagnostico.query.filter_by(incluir_no_algoritmo=1).all()
    incidencias = {diag.cid: Paciente.query.filter_by(cid=diag.cid).count() for diag in diagnosticos}
    total_pacientes = Paciente.query.count()
    prevalencias = {cid: (incidencias[cid] / total_pacientes) * 100 for cid in incidencias}
    return render_template('index.html', incidencias=incidencias, prevalencias=prevalencias)

@app.route('/patients')
def patients():
    page = request.args.get('page', 1, type=int)
    pacientes_query = db.session.query(Paciente, FluxoAtendimento.etapa).join(FluxoAtendimento, Paciente.id == FluxoAtendimento.paciente_id)
    pacientes_pagination = pacientes_query.paginate(page=page, per_page=20)
    next_url = url_for('patients', page=pacientes_pagination.next_num) if pacientes_pagination.has_next else None
    prev_url = url_for('patients', page=pacientes_pagination.prev_num) if pacientes_pagination.has_prev else None
    
    # Obter a lista de CID dos diagnósticos sinalizados
    diagnosticos_sinalizados = [diag.cid for diag in Diagnostico.query.filter_by(incluir_no_algoritmo=1).all()]
    
    return render_template('patients.html', pacientes=pacientes_pagination.items, next_url=next_url, prev_url=prev_url, diagnosticos_sinalizados=diagnosticos_sinalizados)

@app.route('/patient/<int:id>', methods=['GET', 'POST'])
def patient_detail(id):
    paciente = Paciente.query.get_or_404(id)
    fluxo = FluxoAtendimento.query.filter_by(paciente_id=id).first()
    if request.method == 'POST':
        nova_etapa = request.form.get('etapa')
        if nova_etapa:
            fluxo.etapa = nova_etapa
            db.session.commit()
            flash('Etapa da abordagem atualizada com sucesso.')
        return redirect(url_for('patient_detail', id=id))
    return render_template('patient_detail.html', paciente=paciente, fluxo=fluxo)

@app.route('/gerenciar', methods=['GET', 'POST'])
def gerenciar():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'select':
            cids = request.form.getlist('select')
            for cid in cids:
                diagnostico = Diagnostico.query.get(cid)
                if diagnostico:
                    diagnostico.incluir_no_algoritmo = 1
            db.session.commit()
        elif action == 'unselect':
            cids = request.form.getlist('unselect')
            for cid in cids:
                diagnostico = Diagnostico.query.get(cid)
                if diagnostico:
                    diagnostico.incluir_no_algoritmo = 0
            db.session.commit()
        return redirect(url_for('gerenciar'))
    
    diagnosticos_selecionados = Diagnostico.query.filter_by(incluir_no_algoritmo=1).all()
    diagnosticos_nao_selecionados = Diagnostico.query.filter_by(incluir_no_algoritmo=0).all()
    return render_template('gerenciar.html', 
                           diagnosticos_selecionados=diagnosticos_selecionados, 
                           diagnosticos_nao_selecionados=diagnosticos_nao_selecionados)

if __name__ == "__main__":
    app.run(debug=True)
