import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker, unego_get_question, extract_metadata_from_data
from rasa_sdk.events import FollowupAction

center_leading_step = None
unego_question_intro = "제가 질문 한가지 할게요! 질문을 보시고 솔직하게 답변해주시면 됍니다 :)"

logger = logging.getLogger(__name__)


# 추후 밑에 클래스 복사해서 사용
class ActionLeadingCentersIntro(Action):
    def name(self) -> Text:
        return "action_leading_centers_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers_intro')
        # 기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        definedCnt = 0

        # metadata = extract_metadata_from_tracker(tracker)
        # select_metadata = tracker.get_slot('select_metadata')
        # metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

        print("MetaData: ", metadata)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        center_type = center_priority[center_step]
        if center_step == 9:
            return [FollowupAction(name="action_more"), SlotSet("center_step", 0)]
        is_finished = tracker.get_slot('is_finished')
        if is_finished == True:
            if center_step == 0:
                dispatcher.utter_message(
                    f'그럼 센터에 대해 다시 알려드릴게요!'
                )
        # 연료센터
        if center_type == 0:

            if metadata['ct'][0] == 0:
                dispatcher.utter_message(
                    f'당신은 그동안 주변환경이 주는 불편한 압박감으로 인해 늘 뭔 가에 쫓기듯 바쁘게 살아오지 않았나요?')
            elif metadata['ct'][0] == 1:
                dispatcher.utter_message(
                    f'당신은 자신만의 특별한 방식으로 스트레스를 컨트롤하고 오히려 그것을 원동력 삼아 세상으로 나아갈 수 있는 능력을 갖고 태어난 사람입니다. ')
        # 활력센터
        elif center_type == 1:

            if metadata['ct'][1] == 0:
                dispatcher.utter_message(
                    f'당신은 인류의 34%에 속하는 비교적 활력 에너지가 부족한 사람입니다.')
            elif metadata['ct'][1] == 1:
                dispatcher.utter_message(
                    f'당신은 항상 몸에 활력 에너지가 존재하고, 다른 사람들의 지속적인 에너지 사용에 영향을 주는 사람입니다.')
        # 직관센터
        elif center_type == 2:
            if metadata['ct'][2] == 0:
                dispatcher.utter_message(
                    f'당신은 생존에 대한 불안감으로부터 자유로울 수 있는 특별한 사람입니다. 만약 당신이 그렇지 않은 삶을 살고 있다면 마스터봇의 설명을 잘 들어보기 바랍니다.')
            elif metadata['ct'][2] == 1:
                dispatcher.utter_message(
                    f'당신은 직관적으로 무엇이 나의 생존에 도움이 되는지 알아차릴 수 있는 능력을 갖고 태어난 사람입니다.')
        # 감정센터
        elif center_type == 3:
                if metadata['ct'][3] == 0:
                    dispatcher.utter_message(
                        f'당신은 다른 사람들의 감정 에너지에 영향을 받아 때론 억울하게도 다혈질이라는 얘기를 들을 수도 있습니다. 하지만 당신의 온전한 감정 에너지는 매우 평온한 사람입니다.')
                elif metadata['ct'][3] == 1:
                    dispatcher.utter_message(
                        f'당신은 자신만의 감정 에너지를 갖고 있으며 당신이 발신하는 에너지는 다른 사람들의 감정에 영향을 미치도록 디자인되어 있는 사람입니다. 평소에 당신의 감정으로 인해 어려움이 있었다면 마스터봇의 설명에 집중해주기 바랍니다.')
        # 에고센터
        elif center_type == 4:
            if metadata['ct'][4] == 0:
                dispatcher.utter_message(
                    f'당신은 자신을 증명하거나 자신의 존재를 드러내기 위해 애쓸 필요가 없는 사람입니다. 만약 당신이 그렇지 않은 삶을 살고 있다면 마스터봇의 설명을 잘 들어 보기 바랍니다.')
            elif metadata['ct'][4] == 1:
                dispatcher.utter_message(
                    f'당신은 다른 사람들과 약속을 하고 그것을 지키는 과정에서 별다른 스트레스를 받지 않고, 당신의 의지력을 잘 활용할 줄 아는 사람입니다. 만약 당신이 그렇지 않은 삶을 살고 있다면 마스터봇의 설명을 잘 들어보기 바랍니다. ')
        # 방향센터
        elif center_type == 5:
            if metadata['ct'][5] == 0:
                dispatcher.utter_message(
                    f'당신은 자유로운 정체성을 갖을 수 있는 특별한 사람입니다. 만약 당신이 그렇지 않은 삶을 살고 있다면 마스터봇의 설명을 잘 들어보기 바랍니다.')
            elif metadata['ct'][5] == 1:
                dispatcher.utter_message(
                    f'당신은 자신의 정체성에 대한 안정된 확신을 갖고 있는 사람입니다.')

        # 표현센터
        elif center_type == 6:
            if metadata['ct'][6] == 0:
                dispatcher.utter_message(
                    f'당신은 자신의 의견을 말하거나 표현하기 위해 애쓰지 않아도 다른 사람들의 주의를 자연스럽게 끌 수도 있는 특별한 능력을 지닌 사람입니다.')
            elif metadata['ct'][6] == 1:
                dispatcher.utter_message(
                    f'당신은 자신만의 고유한 표현방식이 있고, 언제 표현해야 할 지를 알고 있는 사람입니다. 당신이 이러한 점에서 어려움을 겪고 있다면 마스터봇의 설명을 잘 들어보세요.')
        # 생각센터
        elif center_type == 7:
            if metadata['ct'][7] == 0:
                dispatcher.utter_message(
                    f'당신은 다른 사람이나 다른 무언가로부터 오는 다양한 사고방식에 열려 있고 스폰지처럼 정보를 흡수할 수 있는 사람입니다.')
            elif metadata['ct'][7] == 1:
                dispatcher.utter_message(
                    f'당신은 생각하고 의견을 내는 데에 있어서 자신만의 일정한 방식을 갖고 있고, 자기 신념이 확고한 편입니다. ')
        # 영감센터
        elif center_type == 8:
            if metadata['ct'][8] == 0:
                dispatcher.utter_message(
                    f'당신은 다른 사람이나 다른 무언가로부터 늘 영감을 받는 사람입니다. 또한, ‘누가 나에게 혼란을 주고, 누가 나에게 영감을 주는지 구별할 수 있는 사람이기도 합니다.')
            elif metadata['ct'][8] == 1:
                dispatcher.utter_message(
                    f'당신은 다른 사람들이 무언가에 대해 생각하도록 영감을 주는 사람입니다. 항상 머릿속에 떠오르는 의문에 대한 답을 찾는 사람이기도 합니다.')

        for i in metadata['ct']:
            definedCnt += i

        if leading_priority[0] == 3:
            step = 1
        elif leading_priority[1] == 3:
            step = 2
        elif leading_priority[2] == 3:
            step = 3
        elif leading_priority[3] == 3:
            step = 4

        print("center_leading_step", center_leading_step)

        print("get Step")
        print(tracker.get_slot('step'))
        print("center step", tracker.get_slot('center_step'))
        print("get Step end")
        msg = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        msg5 = ""
        h_center = center_priority[center_step]  # 센터 몇번째까지 했는지를 기준으로 정하는 부분
        center_name = ""
        if h_center == 0 and metadata['ct'][0] == 1:
            h_type = "연료 센터 ( 정의 )"
            center_name = "연료센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            msg = "인류의 60%는 연료센터에서 자신만의 에너지를 발신하며 다른 사람들이 내뿜는 압력에 좌우되지 않고 자신의 고유한 페이스대로 나아갈 수 있는 능력을 갖고 있습니다. "
            msg2 = "당신은 바로 이러한 능력을 가진 사람입니다. 즉, 자신만의 스트레스를 원동력 삼아 세상에 없는 새로운 무엇인가를 만들러 온 사람들이라고 할 수 있습니다."
            msg3 = "연료센터는 3개의 다른 센터와 연결되어 있습니다. 직관센터와 연결되어 있다면 자신만의 정해진 방식으로 스트레스를 사용하여 삶의 잘못된 것들을 고치기 위해 애씁니다. "
            msg4 = "생존 자체를 위해 연료를 사용하고 그것을 통해 살아있음의 기쁨과 즐거움을 느낍니다."
        elif h_center == 1 and metadata["ct"][1] == 1:
            h_type = "활력 센터 ( 정의 )"
            center_name = "활력센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1.gif"
            msg = "당신은 자신이 좋아하는 일을 위해서는 며칠 밤을 새우더라도 괜찮을 수 있는 에너지를 지니고 있습니다. 하지만 이 에너지는 당신이 정말 좋아하는 일을 위해서 사용할 때만 활성화될 수 있습니다. 그렇지 않다면 당신은 만성피로에 시달리는 활력 없는 사람이 되고 말 것입니다. "
            msg2 = "에너지를 활성화시킬 수 있는지 알기 위해서는 주변 사람들에게 “Yes” or “No”로 답이 가능한 형태의 질문을 받아야 합니다. 질문 받은 당신의 몸에서 바로 ‘Yes’라는 반응이 일어나는 일이라면 당신은 늘 활기찰 수 있습니다."
        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            center_name = "직관센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            msg = "당신이 갖고 태어난 능력은 오직 지금 이 순간에만 적용되며 말로는 표현할 수 없는 내면적 인식입니다. 직관(직감)이라는 것은 특히 생명에 직결되고 즉흥적으로 일어나는 정보인데 예를 들면 “느낌이 쎄-해”, “그냥 내 촉이 그래”와 같은 느낌입니다. "
            msg2 = "주의할 점은 직관센터는 한 번 경고를 주고 나면 다시 알려주지 않는다는 점입니다. 처음 직관에서 경고를 했을 때, 그것을 합리화하려는 생각이나 주변 분위기에 맞춰서 타협 혹은 미룰 경우 기회를 놓치게 됩니다. "
            msg3 = "직관센터가 정의되어 있는 당신은, 더더욱 내면에 귀를 기울이고 그 경고를 무시해서는 안 됩니다. 경고를 무시할수록 당신은 자신의 건강을 잃게 됩니다. "
            msg4 = "직관센터의 경고를 신뢰하고 존중할 경우, 선천적인 면역력과 건강을 기반으로 나의 삶에서 위험요소들을 줄일 수 있습니다. "

        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            center_name = "감정센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            msg = "인류의 절반은 자신만의 감정 에너지를 갖고 발신하며 살고 있고, 나머지 절반은 특별한 감정 에너지 없이 다른 절반이 발신하는 감정 에너지에 영향을 받으며 살아가고 있습니다. "
            msg2 = "이러한 감정 에너지와 관련된 센터를 감정센터라고 부릅니다. 감정센터가 정의되어 있는 사람들은 자신만의 감정 에너지의 사이클을 갖도록 디자인된 사람들입니다. "
            msg3 = "당신은 감정센터가 정의되어 있는 사람에 속하므로 자신만의 고유한 감정 에너지의 사이클을 가지며 항상 감정의 업과 다운이 존재함을 느낍니다. "
            msg4 = "당신에게 인내심을 요구하는 것은 쉬운 일이 아닙니다. 당신은 늘 자신의 감정파도 속에서 파도가 높으면 상기되어 고조된 채로 쉽게 결정을 내려버리고, 파도가 낮으면 가라앉은 채로 아무것도 하지 않으려는 무기력한 모습을 보이기 쉽습니다. "

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            center_name = "에고센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            msg = "에고센터는 무언가를 하고 싶은 의지, 용기, 그리고 경쟁을 통해 성취해내는 에너지와 관련된 센터입니다. 이 센터가 정의되어 있는 사람들은 인류의 37% 정도이며 이러한 에너지를 계속 발신하면서 자신만의 의지와 용기로 세상과 맞서 싸우며 살아갑니다. 당신은 에고센터 정의에 해당하므로 이렇게 살아가도록 디자인되어 있습니다."
            msg2 = "당신이 무엇을 입을지, 어디서 일할지, 몇시간이나 일을 할지, 일을 처리하기 위해 시간이 얼마나 필요한지 모든 것을 스스로 통제하고 결정하고 싶어 합니다. 스스로의 가치를 잘 알고 있고 약간은 자신감을 과장하는 경향도 있습니다."

        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            center_name = "방향센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            msg = "당신은 자신의 방향센터에서 에너지를 발신하는 사람입니다. 이것을 방향센터 정의라고 부릅니다. 이러한 부류의 사람들은 사랑받는다는 게 어떤 느낌인지, 사랑을 주는 게 어떤 것인지 자신만의 감각을 가지고 있습니다. "
            msg2 = "자기자신을 아끼고 스스로를 사랑하며 그와 같이 다른 사람들에게도 사랑을 전합니다."
            msg3 = "삶에서 나의 길이 어디를 향하는지 내가 가야 할 방향을 알고 새로운 길을 개척하는 것도 어려움이 없습니다. "
            msg4 = "어디로 가야 하는지 길을 잃은 듯한 다른 사람들에게 안정감을 줄 수도 있고, 더 나아가 인류가 어느 방향을 향해야 하는지 진화하기 위한 길이 무엇인지 전하는 역할을 할 수도 있습니다."


        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            center_name = "표현센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            msg = "당신은 표현센터를 통해 자신만의 고유한 표현방식으로 자신이 원하는 때에 하고 싶은 말이나 표현을 할 수 있는 능력을 타고난 사람입니다. "
            msg2 = "이것을 표현센터가 정의되어 있다고 말합니다. 표현센터는 당신을 구성하는 9개의 센터 중 중심점이고 당신이 가진 모든 것을 모아 당신의 내면을 외부세상에 표현하고 행동하도록 해줍니다."
            msg3 = "무슨 말을 해야 할 지, 어떻게 전달해야 할 지, 언제 표현하는 것이 좋을 지, 자신만의 감각을 가지고 있습니다. "
            msg4 = "하지만 자신만의 감각을 가지고 있는 것이 꼭 좋은 것만은 아닙니다. 표현센터가 어떤 센터에 연결되어 있느냐 에 따라 다양한 상황이 만들어지기 때문입니다."
        elif h_center == 7 and metadata["ct"][7] == 1:
            h_type = "생각 센터 ( 정의 )"
            center_name = "생각센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7.gif"
            msg = "도표나 그림을 떠올리며 생각을 하기도 하고, 어떤 소리가 들려와 생각하기도 하고, 과거에 했던 경험을 바탕으로 생각을 하는 등의 과정을 거쳐 자기만의 의견을 가지게 됩니다."
            msg2 = "이렇게 형성된 당신의 의견은 좀처럼 바뀌지 않고, 외부의 영향에도 잘 흔들리지 않습니다. 하지만, 무언가를 이해하려고 집착적으로 생각하다가 근심에 휩싸일 수 있으니 생각은 생각일 뿐, 행동으로 옮기는 것에는 신중하기 바랍니다. "
        elif h_center == 8 and metadata["ct"][8] == 1:
            h_type = "영감 센터 ( 정의 )"
            center_name = "영감센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8.gif"
            msg = "때때로 과거의 경험이 떠올라 혼란스러울 수 있고, 무언가에 대한 의심이 들고, 알듯 말 듯 한 것을 명확히 알고 싶어지지만 이것은 단지 당신이 세상을 이해하기 위한 현상일 뿐입니다."
            msg2 = "억지로 답을 찾으려는 노력을 하는 동안에는 답이 보이지 않고, 답을 찾기를 멈추었을 때, 답을 보게 될 것입니다."
        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            center_name = "연료센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0_off.png"
            msg = "누구나 갖고 있는 9개의 센터 중에서 연료센터는 우리 몸에 주어지는 육체적 압박감에 대한 에너지와 관련이 있습니다. 당신은 인류의 40%에 해당하는 연료센터가 정의되어 있지 않은 사람에 해당합니다. "
            msg2 = "연료센터는 우리 몸의 아드레날린과 관련이 있는데 연료센터가 미정인 당신은 이것이 꾸준하지 않기 때문에 한 번 일을 시작해도 그것을 오래도록 이어가진 못합니다. "
            msg3 = "그러다 보니 한가지를 진득하게 하기보다는 이것 하다 저것 하다 분주하기만 하기 쉽죠. 초점이 없이 여러가지에 바쁘기만 합니다. "
            msg4 = "당신은 주변의 모든 일을 자신이 받아서 하려고 나서거나 해결할 수 없는 압박감을 해결하기 위해 바쁘곤 합니다. 그러다 보면 결국에는 탈진하거나 번아웃되어 질려버리고 말죠. "
            msg5 = "자각하지 못한 채 외부로부터 들어오는 압박에 의해 자신이 작동되도록 내버려두게 됩니다. 당신이 느끼는 대부분의 압박감은 당신 자신의 것이 아니라는 것을 자각하기 바랍니다."
        elif h_center == 1 and metadata['ct'][1] == 0:
            h_type = "활력 센터 ( 미정의 )"
            center_name = "활력센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1_off.png"
            msg = "더 일하고 싶고, 더 공부하고 싶고, 더 놀고, 더 자고, 더 먹고 싶다 등등 당신은 늘 아쉽습니다. 더 해야 할 것 같고, 더 했으면 좋겠는데 생각과 달리 체력이 따라주지 않습니다."
            msg2 = "그럼에도 늘 ‘더 하고 싶어!! 더 할 거야!!’ 라고 생각하며 늘 지나치게 무언가를 합니다. 자신에게 활력 에너지가 부족함에도 마치 가지고 있는 것처럼 착각하기 쉽습니다."
            msg3 = "당신은 활력 에너지를 통해 생산적인 일을 하는데 적합한 사람이 아니므로 절대 무리하지 말고 되도록 많이 쉬어줄 수 있기를 바랍니다. "
        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            center_name = "활력센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            msg = "인류의 45%는 생존에 대한 두려움이나 불안감에 대한 감각이 거의 없습니다. 반면 나머지 55%는 본능적으로 생존에 대한 위협에 대한 자신만의 감각을 지니고 있습니다. "
            msg2 = "이러한 역할을 담당하는 센터를 직관센터라고 부르고 당신이 속한 45%의 부류를 직관센터가 정의되어 있지 않다, ‘직관센터 미정’이라고 말합니다. "
            msg3 = "즉, 당신의 직관센터는 에너지를 발신하지 않으므로 두려움이나 불안감에 대해 별다른 감각을 갖고 있지 않고, 건강한 상태의 직관센터 미정이라면 오히려 이러한 부분에 대해 편안함을 느끼며 살게 됩니다."
            msg4 = "하지만 우리의 삶은 늘 다른 사람들 과의 관계속에서 이루어지므로 나머지 55%의 사람들이 발신하는 에너지들이 당신과 같은 미정들에게도 영향을 미치게 됩니다. "
            msg5 = "즉, 당신 자신은 별다른 두려움이나 불안감이 없음에도 가까운 사람이 발신하는 에너지를 받거나 심지어 증폭해서 두려움과 불안감을 느끼게 될 수 있습니다."

        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            center_name = "감정센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            msg = "인류의 절반은 자신만의 감정 에너지를 갖고 발신하며 살고 있고, 나머지 절반은 특별한 감정 에너지 없이 다른 절반이 발신하는 감정 에너지에 영향을 받으며 살아가고 있습니다. "
            msg2 = "이러한 감정 에너지와 관련된 센터를 감정센터라고 부릅니다. 감정센터가 정의되어 있는 사람들은 자신만의 감정 에너지의 사이클을 갖도록 디자인된 사람들입니다. "
            msg3 = "나머지 절반의 사람들은 감정센터 미정으로 자신만의 감정 에너지를 발신하지 않고 주변에서 발신하는 감정 에너지의 영향을 받게 됩니다. 물론 좋은 감정 에너지의 발신은 감정센터 미정들에게도 너무나 큰 행복감을 줄 수 있습니다. "
            msg4 = "당신은 감정센터 미정에 속하는 사람이므로 늘 다른 사람들의 감정 에너지 흐름에 민감하고 그것에 좌우되는 경우가 많습니다."

        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            center_name = "에고센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            msg = "에고센터는 무언가를 하고 싶은 의지, 용기, 그리고 경쟁을 통해 성취해내는 에너지와 관련된 센터입니다."
            msg2 = "이 센터가 정의되어 있는 인류의 37%의 사람들은 이러한 에너지를 계속 발신하면서 자신만의 의지와 용기로 세상과 맞서 싸우며 살아갑니다. 하지만 당신이 속한 63%의 사람들은 이러한 경쟁의 부담감으로부터 자유로운 사람들입니다. "
            msg3 = "다른 사람들에게 무엇을 해주어 나의 가치를 인정받고 싶다 거나, 내가 무엇인가를 성취하여 나의 존재를 드러내고 싶다 거나, 지금의 이 경쟁에서 이겨내고 싶다는 부담을 전혀 느낄 필요가 없는 사람들입니다."


        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            center_name = "방향센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            msg = "당신은 고정된 정체성을 갖기 보다는 어느 환경, 어느 자리에서 든 자유롭게 자기 자신을 녹여낼 수 있는 특징을 갖고 있습니다. "
            msg2 = "당신은 자신만의 방향성을 갖고 있기 보다는 다른 사람들의 영향력에 의해 여기저기로 항하게 되며 그러한 과정을 거치면서 자신의 방향으로 점차 맞춰 나갑니다."
            msg3 = "여기저기를 경험하는 동안 자신만의 정체성을 쌓아가며 자신만의 아지트, 집중할 수 있는 곳, 즐겨가는 단골가게 등을 만들어갑니다. 이러한 모든 것들이 모여 당신의 방향을 만들어줍니다."

        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            center_name = "표현센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            msg = "당신이 애쓰지 않고 다른 사람들에 의해 초대되어질 때 가장 자연스럽게 주의가 모아지고, 가장 좋은 타이밍에, 가장 힘들이지 않고, 제일 효과적인 반응을 이끌어낼 수 있습니다."
            msg2 = "억지로 고민하며 말을 하려고 하지도 말고, 침묵의 불편함이 싫어서 불필요한 말을 할 필요도 없고, 뭔가 의견이나 표현이 떠오르면 떠오르는 대로 자연스러운 모습 그대로 있는 것이 좋습니다. 통제하지 않는, 자유로운 목소리가 당신의 진정한 모습입니다."
        elif h_center == 7 and metadata['ct'][7] == 0:
            h_type = "생각 센터 ( 미정의 )"
            center_name = "생각센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7_off.png"
            msg = "당신은 늘 ‘이런 의견도 있구나. 저렇게 생각할 수도 있겠는데? 이 정보도 일리가 있어’ 라고 생각합니다."
            msg2 = "하지만 다른 한편으로는 ‘나는 왜 다 일리가 있다고 할까? 왜 자꾸 생각이나 의견이 바뀌지? 귀가 얇은가?’ 라는 생각도 듭니다. 걱정하지 마세요. 그것이 바로 당신의 건강한 모습입니다."
            msg3 = "당신에게는 어떤 생각이 더 좋은 것이고 어떤 의견이 더 맞는 것인지 구별할 수 있는 잠재력이 있으니 다양한 생각과 의견에 열린 자세를 갖고 살아가기 바랍니다."
        elif h_center == 8 and metadata['ct'][8] == 0:
            h_type = "영감 센터 ( 미정의 )"
            center_name = "영감센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8_off.png"
            msg = "평소에 생각이 많지 않다가 어떤 때는 지나치게 생각이 많아져 머리가 지끈거리거나, 생각을 하고 또 하다가 불면증에 시달린 경험들이 있나요? 이것은 당신 자신으로부터 비롯된 것이 아니라 외부의 영향 때문입니다."
            msg2 = "당신에게는 혼란과 영감을 잘 구별할 수 있는 잠재력이 있습니다."

        dispatcher.utter_message(image=img)
        if msg != "":
            dispatcher.utter_message(msg)
        if msg2 != "":
            dispatcher.utter_message(msg2)
        if msg3 != "":
            dispatcher.utter_message(msg3)
        if msg4 != "":
            dispatcher.utter_message(msg4)
        if msg5 != "":
            dispatcher.utter_message(msg5)

        if h_center == 1 or h_center == 7 or h_center == 8:
            dispatcher.utter_message(f'당신의 {center_name}에 대해 설명해 보았어요.')
            return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                    SlotSet('step', step), FollowupAction(name='action_question_intro')]

        return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                SlotSet("step", step), FollowupAction(name='action_center_detail_intro')]


class ActionLeadingCenters(Action):
    def name(self) -> Text:
        return "action_leading_centers"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers')
        # 기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        definedCnt = 0

        # metadata = extract_metadata_from_tracker(tracker)
        # select_metadata = tracker.get_slot('select_metadata')
        # metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

        print("MetaData: ", metadata)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        if center_step == 9:
            return [FollowupAction(name="action_more")]
        center_priority = tracker.get_slot('center_priority')

        if leading_priority[0] == 3:
            step = 1
        elif leading_priority[1] == 3:
            step = 2
        elif leading_priority[2] == 3:
            step = 3
        elif leading_priority[3] == 3:
            step = 4

        print("center_leading_step", center_leading_step)

        print("get Step")
        print(tracker.get_slot('step'))
        print("center step", tracker.get_slot('center_step'))
        print("get Step end")
        msg = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        msg5 = ""
        center_name = ""
        h_center = center_priority[center_step]  # 센터 몇번째까지 했는지를 기준으로 정하는 부분
        if h_center == 0 and metadata['ct'][0] == 1:
            h_type = "연료 센터 ( 정의 )"
            center_name = "연료센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            msg = "당신의 연료센터가 감정센터와 연결될 경우 개인적 혹은 대인 관계에서의 감정적 스트레스에 대해 스스로의 방식으로 해소할 수 있습니다. 감정적 스트레스를 극복하는 과정을 통해서 더욱 감정에 성숙해지고 다채롭게 드러낼 수 있게 됩니다. "
            msg2 = "연료센터와 연결될 경우, 지나치게 스트레스에 노출되어 강박적인 성향을 가질 수 있습니다. 모든 스트레스에 무차별적으로 과민 반응하며 건강을 축낼 수 있습니다. 이러한 경우 자신의 스트레스를 주변으로 퍼트리지 않도록 주의하기 바랍니다."

        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            center_name = "직관센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            msg = "세상에는 직관센터가 정의되어 있는 당신과 같은 부류의 사람들이 55%, 나머지 45%의 사람들은 직관센터가 미정입니다. 즉, 당신과 같은 생존에 대한 직관이 존재하지 않습니다. "
            msg2 = "따라서, 직관센터 미정인 사람들에게는 직관센터가 정의된 사람이 옆에 함께 있어주는 것만으로도 기분이 좋고 건강이 좋아지는 것 같은 영향을 주기도 합니다."
            msg3 = "당신의 직관센터 에너지가 건강하게 작동할 경우 삶에서 맞닥뜨릴 수 있는 위험요소에 대한 걱정과 두려움은 고민할 필요도 없으며, 그 결과 자연적으로 실존 그 자체를 깊이 경험할 수 있습니다. "
            msg4 = "초 단위로 작동하는 직관센터의 면역체계가 당신을 지켜줍니다. "
        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            center_name = "감정센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            msg = "감정대로 결정을 내리면, 안좋은 일을 Yes 해버리거나 좋은 일을 No 해버리는 경우가 많다는 걸 경험해 보았을거예요. 당신의 감정 사이클이 높지도 않고 낮지 않은 평정심일 때 중요한 결정을 하는 것이 매우 중요합니다. "
            msg2 = "당신의 감정이 어떠한지 알 수 있는 유일한 방법은 그 감정의 파도가 지나간 후에 아까 내가 어떤 상태였구나 (높은 파도였구나, 낮은 파도였구나) 라는 것을 스스로 알아차리는 수 밖에는 없습니다. "
            msg3 = "감정센터의 에너지는 달콤하고, 유혹적이며 강력합니다. 오직 자신의 감정의 흐름만 인내하고 지켜볼 수 있다면 얼마든지 자신에게 유리하게 사용할 수 있다는 겁니다. "
            msg4 = "당신이 감정적으로 명료하게 결정을 내리기 위해 인내하는 시간은 자연스레 다른 사람들에게도 똑같은 기다림의 시간이 되며, 그 기다림의 시간동안 그들은 결국 당신의 그 에너지를, 그 따스함을 더욱 원하게 됩니다. "

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            center_name = "에고센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            msg = "당신은 일하는 것을 즐기는 편이고, 당신 스스로가 모든 것을 통제하고 결정할 수 있을 때 가장 자연스럽고 내면의 힘을 발휘할 수 있습니다. "
            msg2 = "자신의 목표한 것, 약속한 것을 지켜내는 과정을 즐기고, 주변 사람들에게도 그러한 과정을 즐기도록 영향력을 발휘합니다. 자신의 내면에 귀 기울일 때 의지력은 더욱 온전히 발휘되고 일과 휴식의 균형 뿐만 아니라 상황에 맞는 가장 적합한 해결책을 보여줍니다. "
            msg3 = "하지만, 누군가에 의해 무시되거나 거절되어 당신 에고의 의지력이 억눌릴 경우 건강에 안 좋은 영향을 미칩니다. "
            msg4 = "따라서, 무작정 의지력만 믿고 이것저것 일을 벌리거나 실현 가능성이 없는 허무맹랑한 약속만 내걸면서 성취를 이루지 못하고 낭비하게 되면 결국에는 사람들로부터 신뢰를 잃고 누구도 당신을 찾지 않게 될 수도 있음을 명심하기 바랍니다."
        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            center_name = "방향센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            msg = "방향센터 정의의 가장 큰 딜레마는 첫째로 “모든 사람들이 다들 자신이 어디를 향하여 가고 있는지 알고 있을 것이다” 라고 너무나 당연하게 생각한다는 점과, 둘째로 “내가 느끼는(자신이 향하는) 이 방향이 옳은 길이다” 라고 지나치게 다른 사람들에게 밀어붙일 수 있다는 점입니다. "
            msg2 = "모두의 길이 똑같지 않고 각자의 길이 다르다는 점을 이해하지 못한 채 사람들에게 지시하고 방향을 가르쳐주겠다며 이끌려고 할 경우 오히려 분열을 야기하고 불협화음을 만들 수 있습니다. "
            msg3 = "방향센터는 마치 자석처럼 작동하는데 양극을 모두 가지지 않고 한쪽 극만 가지고 있어 끌어당김만이 작용합니다. 바로 사랑이죠. "
            msg4 = "우리는 사랑을 서로 주고 받는 다라고 생각하지만, 실제로 더 정확히는 어느 한쪽이 반드시 더 주도적으로 사랑하게끔 되어있다는 것입니다. "
            msg5 = "특히 주로 방향센터 정의가 사랑을 하는 쪽(주는 쪽)이 되고, 방향센터가 미정인 사람은 그것이 자신의 마음에 들 경우 증폭/반영해주게 되는 것이죠. "
        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            center_name = "표현센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            msg = "당신의 표현센터가 생각센터와 연결되면 자신이 정리한 논리와 개념들, 주장들을 내세우게 됩니다. "
            msg2 = "만약 직관센터와 연결되어 있다면 순간순간의 직감, 특히나 생존이나 안전, 건강에 대한 것들에 대해 표현하려고 합니다. "
            msg3 = "방향센터와 연결되어 있다면 자신의 정체성, 혹은 나아가야 하는 방향에 대해, 사랑에 대해 표현하려 하고, 활력센터와 연결되어 있다면 자신의 활력반응을 그대로 표현하고 실행하게 됩니다."
            msg4 = "에고센터와 연결되어 있다면 자신의 의지/약속을 “나는 이걸 하고 싶어, 저걸 가지고 싶어, 이렇게 이렇게 하겠어” 와 같은 방식으로 드러내게 되고, 감정센터와 연결되어 있다면 나의 감정상태, 기분에 따라 행동하고 이야기합니다."
        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            center_name = "연료센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0_off.png"
            msg = "외부로부터 압박감을 느낄 때는 두가지 방법으로 대처할 수 있습니다. "
            msg2 = "한가지는 그 압박감에 휘둘리지 않고 잠시 자신만의 공간으로 물러나 심호흡 하며 정돈하는 것이고, 다른 하나는 그 압박감에 기꺼이 자신을 내맡겨 상황 자체를 자신에게 유리하게 사용하는 것입니다. "
            msg3 = "대부분의 경우에는 그저 뭔 지 모를 압박감과 불편함에 무엇이라도 하면서 자신을 바쁘게 만들 뿐, 그것이 좋은 성과나 어떤 결과물로 이어지지는 못합니다. "
            msg4 = "오히려 좌충우돌 사고만 치고 사건만 만들기 쉽죠. 당신은 그러한 압박으로부터 자유로울 수 있는 존재라는 것을 잊지 말기 바랍니다."
        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            center_name = "직관센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            msg = "직관센터가 미정인 사람들은 가까운 사람들이 발신하는 에너지에 영향을 받아 안정감을 느끼는 경우가 많습니다. 그것이 그 사람에 대한 의존성을 크게 만들기도 합니다. "
            msg2 = "특히 가족관계나 연인관계에서 더욱 그렇습니다. 그 사람의 존재(영향력)가 나의 생존을 보장해주는 느낌이니까요. "
            msg3 = "이렇게 직관센터가 정의되어 있는 사람의 영향력에 얽매여 있게 된 경우,  그 사람이 주는 직관 정의의 안정감이 너무 크기 때문에 언제 헤어져야 할지, 제대로 관계를 정리해야 할지 모를 수 있습니다."

        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            center_name = "감정센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            msg = "당신의 감정센터는 마치 열려 있는 창문과 같습니다. 여러 감정들을 받아들이고 그것을 분석합니다. 여기서 잊지 말아야 할 점은 객관성을 잃어서는 안 된다는 점입니다. 그 감정에 빠져들거나 개인적인 것으로 받아들여선 안 됩니다. "
            msg2 = "그렇게 되면 창문은 투명성을 잃고, 전체의 감정이 아닌 자신이 원하는 편협하고 일부분의 감정들만 받아들이고, 나머지는 외면하거나 거절하게 됩니다."
            msg3 = "그렇게 점차 자신의 감정상태 뿐만 아니라 주변의 감정 상태에 대해서도 혼란스러움만 커지고 감정 업 다운에 끊임없이 휩쓸릴 경우, 그 불편함을 해소하기 위해 오히려 더욱 과민하게 반응하거나, 별 일 아닌 데도 과장되게 더 억지스럽게 표현하곤 합니다. "
            msg4 = "다른 사람들의 감정에 좌우되지 않도록 주의하기 바랍니다."
        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            center_name = "에고센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            msg = "하지만, 에고센터가 정의되어 있는 사람들과 섞여 살수 밖에 없으므로 그들이 발신하는 에너지를 수신하고 심지어 증폭함으로써 쓸데없는 약속을 하거나 자신을 채찍질하고 밀어붙이는 삶을 살게 되기 쉽습니다. "
            msg2 = "우리가 살아가는 현대사회에서는 항상 “더 빠르고, 예쁘고, 강하고, 성공적이고, 부자일 수 있다!” 라는 에너지로 가득합니다. 에고센터 미정인 당신은 이 에너지 안에 갇혀 함정에 빠진 채 끊임없이 자신을 채찍질하고 밀어붙입니다. "
            msg3 = "자신이 내건 약속을 지키기 위해 이들은 더 큰 약속을 만들기를 반복하고, 결국 자신의 무능력을 느끼며 다시 추락합니다. 실패할 때 마다, 더 상황은 나빠지고 자존감은 바닥에 떨어지게 되죠. "
            msg4 = "당신이 지금 약속을 지키기 위한 큰 부담을 갖고 있거나, 자신의 무능력에 대한 자괴감에 시달리고 있다면, 그러한 부담감이 어디서부터 출발하고 있는지 돌아보면 좋겠습니다. "
            msg5 = "당신은 그러한 것으로부터 자유로운 사람으로 디자인되었음을 다시한번 돌아보기 바랍니다."
        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            center_name = "방향센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            msg = "당신은 특히 장소에 민감합니다. 당신에게 알맞은 장소가 아니라면 그곳에서 만나는 사람들 또한 적합하지 않을 확률이 매우 높습니다. "
            msg2 = "좋은 사람을 만나고 싶다면 당신에게 좋은 느낌을 주는 장소들을 찾아야 합니다. 아무리 좋은 사람을 만나더라도 장소가 마음에 들지 않는다면 그 사람과 어떠한 흐름도 이어지지 않습니다."
            msg3 = "새로운 장소에서 다시 시작해 보세요. 이것이 바로 당신이 자신의 방향을 찾아가는 방법입니다."
        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            center_name = "표현센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            msg = "당신은 다른 사람들의 주의를 끌기 위해 노력하기도 합니다. 다른 사람들이 당신에게 관심을 가져주지 않을까봐 걱정하고 주의를 끌기 위해 노력하는 경우가 있을 수 있습니다. "
            msg2 = "이것은 진정한 모습을 잃어버린 경우입니다. 쓸데없는 말을 많이 하게 되고, 어수선하고 번잡스러운 행동을 하거나, 인상을 남기기 위해 억지 모습을 보이는 것 등이 해당됩니다."

        if msg != "":
            dispatcher.utter_message(msg)
        if msg2 != "":
            dispatcher.utter_message(msg2)
        if msg3 != "":
            dispatcher.utter_message(msg3)
        if msg4 != "":
            dispatcher.utter_message(msg4)
        if msg5 != "":
            dispatcher.utter_message(msg5)

        dispatcher.utter_message(f'당신의 {center_name}에 대해 설명해 보았어요.')
        return [SlotSet("is_question", 0), SlotSet("center_type", h_center), SlotSet("center_step", center_step),
                SlotSet("center_question", True), SlotSet("step", step), SlotSet("is_sentiment", True),
                FollowupAction(name="action_question_intro")]


class ActionLeadingCentersQuestion(Action):
    def name(self) -> Text:
        return "action_leading_centers_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers_question')

        # metadata = extract_metadata_from_tracker(tracker)
        # select_metadata = tracker.get_slot('select_metadata')
        # metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

        print("MetaData: ", metadata)
        step = tracker.get_slot('step')

        return [SlotSet('step', step), SlotSet("center_question", False), FollowupAction(name='action_more')]


class ActionCenterDetailIntro(Action):
    def name(self) -> Text:
        return "action_center_detail_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_center_detail_intro')
        # 자세히 설명하기 위한 인트로 (센터별로 다르기때문에 새로 구현)
        # metadata = extract_metadata_from_tracker(tracker)
        # select_metadata = tracker.get_slot('select_metadata')
        # metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

        center_step = tracker.get_slot("center_step")
        center_priority = tracker.get_slot('center_priority')
        h_center = center_priority[center_step]

        buttons = []
        buttons.append({"title": f'네. 듣고 싶어요', "payload": "/leading_centers"})
        buttons.append({"title": f'아뇨 괜찮아요', "payload": "/question_intro"})

        if h_center == 0 and metadata['ct'][0] == 1:
            h_type = "연료 센터 ( 정의 )"
            dispatcher.utter_message("다른 두개의 센터와의 관계도 설명해 볼까요?", buttons=buttons)
        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            dispatcher.utter_message("직관센터는 당신의 건강과 밀접합니다. 좀더 설명을 들으시겠어요?", buttons=buttons)

        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            dispatcher.utter_message("감정의 사이클이라는 것이 좀 어색하죠? 조금더 설명을 들어보시겠어요?", buttons=buttons)

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            dispatcher.utter_message("자, 에고센터 정의인 사람들에 대해 좀더 설명해볼까요?", buttons=buttons)
        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            dispatcher.utter_message("자, 당신의 방향센터에 대해 이해가 되셨나요? 당신이 갖게 되는 딜레마에 대해서도 설명해 볼까요?", buttons=buttons)
        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            dispatcher.utter_message("어떤 상황들이 있을 수 있는지 좀더 얘기해 볼까요?", buttons=buttons)



        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            dispatcher.utter_message("자, 이제는 극복할 수 있는 방법에 대해 좀더 얘기해볼까요?", buttons=buttons)
        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            dispatcher.utter_message("자, 당신이 알아야 할 점을 좀더 얘기해 볼까요?", buttons=buttons)
        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            dispatcher.utter_message("자, 감정센터와 관련되어 조심할 점을 좀더 얘기해 볼까요?", buttons=buttons)
        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            dispatcher.utter_message("자, 에고센터 미정인 사람들이 빠지기 쉬운 함정에 대해 좀더 설명해줄까요?", buttons=buttons)
        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            dispatcher.utter_message("자, 당신의 정체성과 방향성에 대해 이해가 되었나요? 당신에 대해 흥미로운 조언을 좀더 해드릴까요?", buttons=buttons)
        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            dispatcher.utter_message("당신의 좋은 모습을 이해할 수 있겠죠? 좋지 않은 모습에 대해서도 알려줄까요?", buttons=buttons)

        return []
# class ActionCenterMore(Action):
#    def name(self) -> Text:
#        return "action_center_more"

#    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#        print('action_center_more')
