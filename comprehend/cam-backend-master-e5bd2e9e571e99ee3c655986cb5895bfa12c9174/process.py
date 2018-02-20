import comprehender
import ItemSearch
import deserializer as ds


TEST_TEXT="""
People have known since ancient times that aspirin helps to reduce pain and high body temperature. But that is not all aspirin can do. It has gained important new uses in recent years. Small amounts of the drug may help prevent a heart attack or stroke.

One study showed that some people who took two aspirin pills a day had lower rates of colorectal cancer. And researchers say aspirin may help patients with colon cancer live longer. But others say the acid in aspirin can cause bleeding in the stomach and intestines. And studies showed that aspirin or other pain medicines may lead to loss of eyesight and hearing.

So, how did aspirin become so important? The story begins with a willow tree. Two thousand years ago, the Greek doctor Hippocrates advised his patients to chew on the bark and leaves of the willow. The tree contains the chemical salicin. In the 1800s, researchers discovered how to make salicylic acid from salicin. In 1897, a chemist named Felix Hoffmann at Friedrich Bayer and Company in Germany created acetyl salicylic acid. Later, it became the active substance in a medicine that Bayer called aspirin.

In 1982, a British scientist shared the Nobel Prize in Medicine in part for discovering how aspirin works. Sir John Vane found that aspirin blocks the body from making natural substances called prostaglandins. Prostaglandins have several effects on the body. Some cause pain and the expansion, or swelling, of damaged tissue. Others protect the lining of the stomach and small intestine. Prostaglandins make the heart, kidneys and blood vessels work well.

But there is a problem. Aspirin works against all prostaglandins, good and bad. Scientists have also learned how aspirin interferes with an enzyme. One form of this enzyme makes the prostaglandin that causes pain and swelling. Another form creates a protective effect. So aspirin can reduce pain and swelling in damaged tissues. But it can also harm the inside of the stomach and small intestine. And sometimes it can cause bleeding.

Many people take aspirin to reduce the risk of a heart attack or stroke from blood clots. Clots can block the flow of blood to the heart or brain and cause a heart attack or stroke. Scientists say aspirin prevents blood cells called platelets from sticking together to form clots.

A California doctor named Lawrence Craven first reported this effect in the 1950s. He observed unusual bleeding in children who chewed on an aspirin product to ease the pain after a common operation. Doctor Craven believed the bleeding took place because aspirin prevented blood from thickening. He thought this effect might help prevent heart attacks caused by blood clots. He examined the medical records of 8,000 aspirin users and found no heart attacks in this group. He invited other scientists to test his ideas. But it was years before large studies took place.

Charles Hennekens of Harvard Medical School led one of the studies. In 1983, he began to study more than 22,000 healthy male doctors over 40 years of age. Half took an aspirin every other day. The others took what they thought was aspirin. But it was only a placebo, an inactive substance. Five years later, Dr. Hennekens reported that people who took aspirin reduced their risk of a heart attack. But they had a higher risk of bleeding in the brain than the other doctors.

A few years ago, a group of experts examined studies of aspirin at the request of federal health officials in the United States. The experts said people with an increased risk of a heart attack should take a low-strength aspirin every day. Aspirin may help someone who is having a heart attack caused by a blockage in a blood vessel. Aspirin thins the blood, so the blood may be able to flow past the blockage. But experts say people should seek emergency help immediately. And they say an aspirin is no substitute for treatment, only a temporary help. 

"""
category = 'HealthPersonalCare'
TEST_TEXT2 = "Samsung is an amazing company. I am so happy they have the worst products. LIke the SamsUng Gear VR wo w it is ssssss so good!!!! and also. Samsung rocks my sox off. The best monitor and gaming console go well with the samsungs."
c = comprehender.Comprehender()
kp = c.comprehend_key_phrases(TEST_TEXT)
ent = c.comprehend_entities(TEST_TEXT)
item_searcher = ItemSearch.ItemSearch(category,ent,kp)
item_searcher.naive_parse()
results = item_searcher.search()

def p(r):
    for i in r:
        print(i)

