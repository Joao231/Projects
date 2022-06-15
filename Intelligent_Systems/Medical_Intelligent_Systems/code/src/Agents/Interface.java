package Agents;

import java.awt.Color;
import java.awt.Dimension;
import java.io.Serializable;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import Classes.Farm;
import Classes.Position;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.UnreadableException;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartFrame;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.labels.PieSectionLabelGenerator;
import org.jfree.chart.labels.StandardPieSectionLabelGenerator;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PiePlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.category.CategoryItemRenderer;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.data.general.DefaultPieDataset;

import com.orsoncharts.plot.PiePlot3D;

public class Interface extends Agent {
	private Map<String,Farm> Farmacias = new HashMap<>() ;
	//private Map<String,Integer> dic;
	private String farmaciaComMaisPedidos;
	private String farmacia_maior_lucro;
	
	private static final long serialVersionUID = 1L;
	protected void setup() {
		super.setup();
		
		System.out.print(
				"#########################################################################   Starting Interface    ##################################################################\n");

		System.out.print("\n");
	
		//Behaviours
		
		addBehaviour(new ContactarFarmacias());
		addBehaviour(new Receiver());
	}
	
	private class ContactarFarmacias extends OneShotBehaviour {
		private static final long serialVersionUID = 1L;
		private int numFarmacias;
		
		public void action() {

			try {
				// Contactar todas as farmácias
				DFAgentDescription dfd = new DFAgentDescription();
				ServiceDescription sd = new ServiceDescription();
				sd.setType("Farmacia");
				dfd.addServices(sd);

				DFAgentDescription[] result = DFService.search(this.myAgent, dfd);
				String[] farmacias; //array de AID das farmacias
				farmacias = new String[result.length]; //array de AID das farmacias com tamanho do array result
				numFarmacias = result.length;

				for (int i = 0; i < result.length; ++i) {
					farmacias[i] = result[i].getName().getLocalName(); //introduz no array farmacia o nome de cada farmacia
					
					//envia msg a cada farmacia para ela enviar as suas coordenadas
					ACLMessage mensagem = new ACLMessage(ACLMessage.PROPOSE);
					AID receiver = new AID();
					receiver.setLocalName(farmacias[i]);
					mensagem.addReceiver(receiver);
					myAgent.send(mensagem); 
					}
				
				} catch (FIPAException e) {
				e.printStackTrace();
				}
			}
		}
	
	private class Receiver extends CyclicBehaviour { 

		private static final long serialVersionUID = 1L;
		private String ID_Farmacia;
		private String Pedido;
		private double tempo;
		private String[] med,med1,med2,med3;
		private Integer[] stock2;
		private int xFarmacia, yFarmacia, xCidadao, yCidadao;
		private int minDistance = 1000;
		private String customerName;
		
		@SuppressWarnings("unchecked")
		public void action() {
			
			ACLMessage msg = receive();
			if (msg != null) {
				
				//Recebe coordenadas de cada farmácia
				if (msg.getPerformative() == ACLMessage.SUBSCRIBE) {
					AID Farmacia2 = msg.getSender();
					String ID_Farmacia= msg.getSender().getLocalName();
					
					//Cria uma nova Class_Farmacia guardando no arraylist Farmacias
					try {
						Farm a = (Farm) msg.getContentObject();
						Farmacias.put(ID_Farmacia,a);

					} catch (UnreadableException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
					
				if (msg.getPerformative() == ACLMessage.INFORM) {
					
					try {
						HashMap<String, Farm> farmacias = (HashMap<String, Farm>) msg.getContentObject();
									
						farmacia_maior_lucro = "";
						int lucro = 0;
						
						farmaciaComMaisPedidos = "";
						int pedido = 0;
						
						System.out.print(
								"********************************************************************************************************************************************************************\n");
						
						System.out.print(
								"                                                                               STOCK DAS FARMÁCIAS                                                                  \n");
						System.out.print(
								"********************************************************************************************************************************************************************\n");
						
						System.out.print(
								"+------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n");
						
						System.out.print(
								"|  FARMÁCIA  |  Brufen  | Ben-u-ron |  Aspirina  |  Xanax  |  Valium  | Fenistil | Voltaren |  Buscopan  | Leite NAN | Kompensan |  Rennie  | Bissolvon | Strepfen |\n");
						
						for(HashMap.Entry<String, Farm> pair  : farmacias.entrySet()) {
							Farm f=pair.getValue();
														
							HashMap<String, Integer> stock4 =  f.getStock_medicamentos(); //Obter a lista dos seus stocks
							
							System.out.print(
									"+------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n");
							System.out.print("|  "+pair.getKey().toUpperCase()+" |    " + stock4.get("brufen") + "     |     "
									+ stock4.get("ben-u-ron") + "     |     "
									+ stock4.get("aspirina") + "      |    " + stock4.get("xanax") 
									+ "    |    " + stock4.get("valium") + "     |     " + stock4.get("fenistil") + "    |    " 
									+ stock4.get("voltaren")+ "     |     " + stock4.get("buscopan") 
									+ "      |     " + stock4.get("leite NAN") + "     |     " + stock4.get("kompensan") + "     |     " 
									+ stock4.get("rennie") + "    |     " + stock4.get("bissolvon") + "     |     " 
									+ stock4.get("strepfen") + "    |     " 
									+ " \n");
							
							}
						System.out.print(
								"+------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n");
						
						System.out.print("\n");
						System.out.print("\n");
						System.out.print("\n");
												
						System.out.print(
								"********************************************************************************************************************************************************************************************\n");
						
						System.out.print(
								"                                                                              Nº DE VENDAS                                                                         \n");
						System.out.print(
								"********************************************************************************************************************************************************************************************\n");
						
						System.out.print(
								"+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n");
												
						System.out.print(
								"|  FARMÁCIA  |  Brufen  | Ben-u-ron |  Aspirina  |  Xanax  |  Valium  | Fenistil | Voltaren |  Buscopan  | Leite NAN | Kompensan |  Rennie  | Bissolvon | Strepfen |    Total de vendas    |\n");
						
						DefaultCategoryDataset dados = new DefaultCategoryDataset();

						for(HashMap.Entry<String, Farm> pair  : farmacias.entrySet()) {
							Farm f=pair.getValue();
							String nome_farmacia= f.getAgent().getLocalName();
							dados.setValue(f.getProdutos_vendidos().get("brufen"), "brufen", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("ben-u-ron"), "ben-u-ron", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("aspirina"), "aspirina", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("xanax"), "xanax", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("valium"), "valium", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("fenistil"), "fenistil", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("voltaren"), "voltaren", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("buscopan"), "buscopan", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("leite NAN"), "leite NAN", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("kompensan"), "kompensan", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("rennie"), "rennie", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("bissolvon"), "bissolvon", nome_farmacia);
							dados.setValue(f.getProdutos_vendidos().get("strepfen"), "strepfen", nome_farmacia);
														
							HashMap<String, Integer> produtos_vendidos =  f.getProdutos_vendidos(); //Obter a lista dos seus stocks
							int soma = 0;
							for(HashMap.Entry<String, Integer> conjunto  : produtos_vendidos.entrySet()) {
								soma += conjunto.getValue();
							}
							
							System.out.print(
									"+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n");
							System.out.print("|  "+pair.getKey().toUpperCase()+" |    " + produtos_vendidos.get("brufen") + "     |     "
									+ produtos_vendidos.get("ben-u-ron") + "     |     "
									+ produtos_vendidos.get("aspirina") + "      |    " + produtos_vendidos.get("xanax") 
									+ "    |    " + produtos_vendidos.get("valium") + "     |     " + produtos_vendidos.get("fenistil") + "    |    " 
									+ produtos_vendidos.get("voltaren")+ "     |     " + produtos_vendidos.get("buscopan") 
									+ "      |     " + produtos_vendidos.get("leite NAN") + "     |     " + produtos_vendidos.get("kompensan") + "     |     " 
									+ produtos_vendidos.get("rennie") + "    |     " + produtos_vendidos.get("bissolvon") + "     |     " 
									+ produtos_vendidos.get("strepfen") + "    |          " + soma + "            |    "
									+ " \n");
							}
						
						JFreeChart chart = ChartFactory.createBarChart(" Vendas por Farmacia ", "Farmacias", "Vendas", dados, PlotOrientation.VERTICAL, true, true, false);
						ChartFrame frame1 = new ChartFrame("Gráfico de barras", chart);
						frame1.setVisible(true);
						frame1.setBounds(300, 0, 1000, 450);
						
						System.out.print(
								"+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n");
						
						System.out.print("\n");
						System.out.print("\n");
						System.out.print("\n");
						
						System.out.print(
								"**************************************************************************************************************************************\n");
						
						System.out.print(
								"                                                    Histórico de Pacientes por Farmácia                                                                        \n");
						System.out.print(
								"**************************************************************************************************************************************\n");
						
						System.out.print(
								"+------------------------------------------------------------------------------------------------------------------------------------+\n");
						
						System.out.print(
								"|  FARMÁCIA  |  Cidadao0  | Cidadao1 |  Cidadao2  |  Cidadao3  |  Cidadao4  | Cidadao5 | Cidadao6 |  Cidadao7  | Cidadao8 | Cidadao9 |\n");
						
						DefaultCategoryDataset dados3 = new DefaultCategoryDataset();

						for(HashMap.Entry<String, Farm> pair  : farmacias.entrySet()) {
							Farm f=pair.getValue();
							HashMap<String, Integer> farm_cidadao =  f.getCidadaos(); //Obter a lista dos seus stocks
							
							String nome_farmacia= f.getAgent().getLocalName();
							int max = 0;
							String cidadao = "";
							for(HashMap.Entry<String, Integer> conjunto  : farm_cidadao.entrySet()) {
								 
								int cidadao_vend = conjunto.getValue();
								if (cidadao_vend>max){
									cidadao = conjunto.getKey();
									max = cidadao_vend;
								}
							}
							
							if (max!=0) {
								dados3.setValue(max, nome_farmacia, cidadao);
							}
							
							System.out.print(
									"+------------------------------------------------------------------------------------------------------------------------------------+\n");
							System.out.print("|  "+pair.getKey().toUpperCase()+" |     " + farm_cidadao.get("Cidadao0") + "      |     "
									+ farm_cidadao.get("Cidadao1") + "    |     "
									+ farm_cidadao.get("Cidadao2") + "      |      " + farm_cidadao.get("Cidadao3") 
									+ "     |      " + farm_cidadao.get("Cidadao4") + "     |     " + farm_cidadao.get("Cidadao5") + "    |    " 
									+ farm_cidadao.get("Cidadao6")+ "     |     " + farm_cidadao.get("Cidadao7") 
									+ "      |     " + farm_cidadao.get("Cidadao8") + "    |     " + farm_cidadao.get("Cidadao9") + "    |     " + "\n");
							
							}
						
						JFreeChart chart3 = ChartFactory.createBarChart(" Cliente mais requisitado por Farmácia ", "Farmacias", "Vendas", dados3, PlotOrientation.VERTICAL, true, true, false);
						ChartFrame frame3 = new ChartFrame("Gráfico de barras", chart3);
						frame3.setVisible(true);
						frame3.setBounds(1000, 500, 450, 450);
						
						System.out.print(
								"+------------------------------------------------------------------------------------------------------------------------------------+\n");
						
						System.out.print("\n");
						System.out.print("\n");
						System.out.print("\n");							
						
						System.out.print(
								"|  FARMÁCIA  |   Lucro   |  Pedidos  |");
						System.out.print(
								"\n");
						System.out.print(
								"+------------------------------------+\n");
						
						DefaultPieDataset dados2 = new DefaultPieDataset();

						for(HashMap.Entry<String, Farm> pair  : farmacias.entrySet()) {
							Farm f=pair.getValue();
							int lucro2 = f.getReceita() - f.getDespesa();
							
							int pedido2= f.getPedidos();
							
							String nome_farmacia= f.getAgent().getLocalName();
							if (lucro2>0) {
								dados2.setValue(nome_farmacia, lucro2);
							}
							
							System.out.print("|  "+pair.getKey().toUpperCase()+" |    " + lucro2 + "    |      " + pedido2 + "      |");
							System.out.print(
									"\n");	
							
							if (lucro2 == lucro) {
								farmacia_maior_lucro+=" e ";
								farmacia_maior_lucro+=pair.getKey();
							}
							
							if (lucro2 > lucro) {
								lucro=lucro2;
								farmacia_maior_lucro=pair.getKey();
							}
							
							if (pedido2 == pedido) {
								farmaciaComMaisPedidos+=" e ";
								farmaciaComMaisPedidos+=pair.getKey();
							}
							
							if (pedido2 > pedido) {
								pedido=pedido2;
								farmaciaComMaisPedidos=pair.getKey();
							}
							
						}
						
						JFreeChart chart2 = ChartFactory.createPieChart(" Lucro por Farmácia ", dados2, true, true, false);
						PiePlot plot = (PiePlot) chart2.getPlot();
				        				        
				        plot.setSimpleLabels(true);
				        PieSectionLabelGenerator gen = new StandardPieSectionLabelGenerator(
				                "{0}: {1}€ ({2})", new DecimalFormat("0"), new DecimalFormat("0%"));
				            plot.setLabelGenerator(gen);
						
						ChartFrame frame2 = new ChartFrame("Gráfico circular", chart2);
						frame2.setVisible(true);
						
						frame2.setBounds(0, 500, 450, 450);
						
						System.out.print(
								"+------------------------------------+\n");
						
						System.out.print("\n");
						System.out.print("\n");
						System.out.print("\n");
						
						System.out.println("A farmacia com maior lucro é: " + farmacia_maior_lucro + " com " + lucro + " euros!");
						
						System.out.println("A farmacia com maior numero de pedidos é: " + farmaciaComMaisPedidos + " com " + pedido + " pedido(s)!");
						
						System.out.print("\n");

					}
					catch (UnreadableException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			}
			else {
				block();
			}
		}
	}	
}

