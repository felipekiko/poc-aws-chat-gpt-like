import json
import boto3
import os
import random
import time

def lambda_handler(event, context):
    apigw_management = None

    for record in event['Records']:
        msg = json.loads(record['body'])
        connection_id = msg['connection_id']
        domain = msg['domain']
        stage = msg['stage']
        prompt = msg['prompt']

        if not apigw_management:
            apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=f"https://{domain}/{stage}")

        # ------ Simulando o processamento do prompt: INICIO ------ #
        resposta = f"Ash Ketchum nasceu e cresceu na pacata Cidade de Pallet, na região de Kanto, e desde pequeno nutria o sonho de se tornar um Mestre Pokémon, inspirado pelos campeões que via na televisão e pelas histórias de aventuras contadas por outros treinadores. No dia de seu aniversário de dez anos, quando finalmente poderia receber seu primeiro Pokémon, Ash acabou dormindo demais e chegou atrasado ao laboratório do Professor Carvalho, onde todas as três escolhas tradicionais – Bulbasaur, Charmander e Squirtle – já haviam sido entregues a outros iniciantes. Como única opção, restava-lhe Pikachu, um Pokémon elétrico rebelde que se recusava a entrar em sua Pokébola e a obedecer ordens. Apesar da relação inicial turbulenta, marcada por desentendimentos e a teimosia de ambos, um episódio em que Ash arrisca a própria vida para proteger Pikachu de um bando de Spearows acaba selando a amizade dos dois, e a faísca dessa relação se transformaria na chama que guiaria toda a sua trajetória. Assim começa a grande jornada, com Ash viajando por Kanto em busca das insígnias de ginásio necessárias para competir na Liga Pokémon. Ao longo do caminho, ele conhece Misty, líder de ginásio especializada em Pokémon aquáticos, que o acompanha após um acidente em sua bicicleta, e Brock, líder de ginásio especialista em Pokémon de pedra, que decide viajar com ele para se tornar um grande criador Pokémon. Os três compartilham inúmeras aventuras, enfrentando constantemente a Equipe Rocket, composta por Jessie, James e Meowth, vilões atrapalhados que perseguem Pikachu de forma obsessiva, mas sempre acabam derrotados. Ash conquista insígnias, fortalece seus laços com Pikachu e outros Pokémon capturados, e participa da Liga de Kanto, onde, apesar de mostrar determinação, é eliminado antes de chegar à final. Essa primeira derrota, longe de desanimá-lo, planta a semente de sua resiliência e da filosofia que seguiria para sempre: cada fracasso é apenas um degrau na escada para a vitória. A aventura continua em Johto, onde Ash mantém sua amizade com Misty e Brock, explorando uma nova região cheia de espécies inéditas de Pokémon. Durante essa fase, Ash demonstra amadurecimento como treinador, refinando suas estratégias e aprendendo a lidar melhor com derrotas e vitórias. Ele conhece novos rivais, enfrenta ginásios desafiadores e consegue alcançar um desempenho mais sólido na Liga de Johto, ainda que não chegue ao título. Essa jornada reforça a ideia de que crescer significa não apenas colecionar vitórias, mas também evoluir ao lado dos Pokémon, aprendendo com cada batalha. Em Hoenn, Ash parte com Brock e conhece May e Max, dois irmãos que passam a acompanhá-lo. May, inicialmente sem interesse por batalhas, encontra sua paixão nos Concursos Pokémon, inspirando-se em Ash e criando sua própria trajetória. Essa fase mostra como Ash não só cresce, mas também inspira outros a seguirem sonhos próprios. Ele enfrenta novos rivais, desafia ginásios e se torna mais estratégico e habilidoso, consolidando-se como um treinador respeitado. Sua participação na Liga de Hoenn mostra novamente sua evolução, mas também os limites que ainda precisava superar. Em Sinnoh, talvez um dos momentos mais memoráveis de sua carreira, Ash conhece Dawn, uma coordenadora Pokémon entusiasmada, e reencontra Brock. Essa jornada é marcada por batalhas intensas e pelo surgimento de Paul, um rival que contrasta completamente com Ash em filosofia: enquanto Ash acredita na amizade, confiança e parceria com seus Pokémon, Paul adota uma abordagem fria e calculista, tratando os Pokémon apenas como ferramentas para a vitória. Essa rivalidade leva Ash a se superar em um dos arcos mais elogiados da franquia, culminando em uma batalha espetacular na Liga de Sinnoh, onde Ash, apesar de ser derrotado, mostra um desempenho impecável e prova seu amadurecimento. Em Unova, Ash embarca em uma nova aventura, encontrando companheiros como Iris e Cilan. Embora essa fase seja vista por alguns fãs como uma regressão em sua experiência, Ash ainda mostra perseverança e espírito competitivo, conquistando insígnias e participando da Liga local. No entanto, é em Kalos que Ash atinge um de seus auges como treinador. Ao lado de Serena, Clemont e Bonnie, Ash apresenta maturidade, estratégia e um vínculo profundo com seus Pokémon, especialmente com Greninja, com quem desenvolve uma conexão única conhecida como Forma Ash-Greninja. Essa ligação é símbolo da evolução de Ash como treinador e como pessoa, mostrando sua capacidade de se conectar com seus parceiros em um nível quase espiritual. Na Liga de Kalos, Ash chega à final em uma batalha lendária contra Alain e seu Mega Charizard X, proporcionando um dos confrontos mais emocionantes de toda a franquia, ainda que termine novamente sem a vitória. A virada decisiva ocorre em Alola, onde Ash adota um estilo de vida diferente, estudando na Escola Pokémon e vivendo aventuras menos tradicionais, sem ginásios formais. Ao lado de amigos como Lillie, Kiawe, Mallow e Sophocles, Ash aprende novas lições sobre convivência, responsabilidade e confiança. Sua jornada culmina na Liga de Alola, onde, pela primeira vez em sua história, Ash conquista o título de campeão, um momento que emocionou milhões de fãs ao redor do mundo e marcou um ponto de virada em sua trajetória. Finalmente, em Galar, Ash participa da Copa dos Campeões, um torneio mundial que reúne os maiores treinadores do planeta. Nessa competição, Ash enfrenta adversários poderosos, incluindo campeões renomados de outras regiões, e mostra toda a experiência acumulada ao longo de anos de jornadas. Sua batalha final contra Leon, o campeão invicto e símbolo máximo de força em Galar, é um dos momentos mais épicos da franquia. Com a ajuda de Pokémon como Lucario, Dragonite, Gengar e, claro, Pikachu, Ash consegue derrotar Leon em uma batalha memorável, consagrando-se como Campeão Mundial e finalmente realizando o sonho que carregava desde os seus dez anos. Essa conquista não é apenas a coroação de um percurso cheio de desafios, derrotas e vitórias, mas também um símbolo do crescimento de Ash como pessoa: o garoto desajeitado que saiu atrasado no dia em que começou sua jornada se tornou um treinador respeitado mundialmente, reconhecido não apenas pela força em batalhas, mas pela forma como trata seus Pokémon, pela inspiração que transmite a amigos e rivais e pela determinação incansável em perseguir seu sonho. Ao longo de sua trajetória, Ash mostrou que ser um Mestre Pokémon não significa apenas vencer batalhas, mas também valorizar a amizade, aprender com os erros e acreditar sempre no poder dos laços que nos unem."
        palavras = resposta.split()
        partes = []
        i = 0

        while i < len(palavras):
            grupo = random.randint(2, 5)
            partes.append(' '.join(palavras[i:i+grupo]))
            i += grupo

        for parte in partes:
            apigw_management.post_to_connection(
                Data=json.dumps({'type': 'stream', 'chunk': parte}),
                ConnectionId=connection_id
            )
            time.sleep(0.5)
        # ------ Simulando o processamento do prompt: FIM ------ #

        apigw_management.post_to_connection(
            Data=json.dumps({'type': 'end'}),
            ConnectionId=connection_id
        )
