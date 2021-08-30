import sys
sys.path.append('.')

import re
import core

matches = """
Free Agent BestNess (Ness) vs Bandits Sonix (Sonic) Grand Final
8BitMan (R.O.B.) vs Bandits Sonix (Sonic) Losers Semis
Bandits Sonix (Sonic) vs Sharp (Pyra Mythra, Wolf) Losers Quarters
SassyFlygon (Luigi) vs BestNess (Ness, Piranha Plant) Winners Finals
SassyFlygon (Luigi) vs Bandits Sonix (Sonic) Losers Finals
SassyFlygon (Luigi) vs 8BitMan (R.O.B.) Winners Semis
Bandits Sonix (Sonic) vs Free Agent BestNess (Ness) Winners Semis
Grayclash (Bayonetta) vs 8BitMan (Diddy Kong) Losers Quarter
Kagaribi 4 Losers Semis - Zackray (Joker) Vs. Hero (Bowser) SSBU Smash Ultimate
CEO 2019 SSBU - FOX | MkLeo (Joker) Vs. PG | Marss (ZSS, Falcon) Smash Ultimate Grand Finals
Frostbite 2020 SSBU Losers Top 32 - MkLeo (Joker) Vs MVG | Salem (Hero, Dark Samus) Ultimate Singles
zackray vs MastaMario - Pools Winners' Semifinals: Ultimate Singles - TBH9 | Joker vs Mario
MSM Online 22 - Ashton (Young Link) Vs. NEST | Sharp (Joker) Grand Finals - Smash Ultimate
【#スマブラSP/#マエスマ】＜準決勝＞ひがちゃんまる(ガノンドロフ）VS そめ(ゲッコウガ)【1on1#226 オンライン大会/SSBU Online Tournament】
SNS5 SSBU - CLG | VoiD (Pichu) Vs. MVG | Dark Wizzy (Mario) Smash Ultimate Winner's Top 64
Genesis 6 - TSM | Leffen (Pokemon Trainer) vs dB | yeti (Mega Man) Top 32 - Smash Ultimate
The Grind 144 GRAND FINALS - Dexter (Wolf) Vs. Mj [L] (ROB) Smash Ultimate - SSBU
"""

test = '【#スマブラSP/#マエスマ】＜準決勝＞ひがちゃんまる(ガノンドロフ）VS そめ(ゲッコウガ)【1on1#226 オンライン大会/SSBU Online Tournament】'


def main():
    # get_name('ガノンドロフ')
    for row in matches.splitlines():
        print(core.video.match_parser.parse(row))


main()