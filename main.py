import nextcord
import json
import requests
import os
import zipfile
client = nextcord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
allowed_ids = {
    "0WON": 462149045268512768,

}
admin= {
    "0WON": 462149045268512768,
    "Dudals": 390048359089569793,
}
allowed_set = set()
admin_set =set()
for id in admin.values():
        admin_set.add(id)
for id in allowed_ids.values():
        allowed_set.add(id)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!add"):
        if message.author.id in list(admin_set):
            add_id = message.content.replace("!add","").replace("<@!","").replace(">","").replace(" ","")
            print(add_id)
            await message.channel.send(f"adding <@!{add_id}>")
            allowed_set.add(add_id)
        else:
            await message.channel.send("권한이 없으시네영")
    if message.content.startswith('!ping'):
        await message.channel.send('pong!')
    if message.content.startswith("!mod"):
        print(message.author.id)
        def is_correct(m):
            return m.author == message.author and m.content
        embed = nextcord.Embed(title="모드제어판", description="factorio.0won.org 모드 제어판입니다", color=0x8080ff)
        embed.add_field(name="1. 모드설정", value="모드를 추가/제거합니다", inline=False)
        embed.add_field(name="2. 모드상황", value="활성화된 모드를 보여줍니다", inline=False)
        embed.add_field(name="3. 종료", value="모드 수정을 취소합니다", inline=False)
        embed.add_field(name="4. 권한요청", value="모드 수정 권한을 요청합니다", inline=False)
        await message.channel.send(embed=embed)
        agreement1 = await client.wait_for('message', check=is_correct, timeout=30.0)
        if agreement1.content == "1":
                if message.author.id in list(allowed_set):
                    embed1 = nextcord.Embed(title="모드설정", description="factorio.0won.org 모드 설정입니다", color=0xff99cc)
                    embed1.add_field(name="1. 모드추가", value="모드를 추가합니다", inline=False)
                    embed1.add_field(name="2. 모드제거", value="모드를 제거합니다", inline=False)
                    embed1.add_field(name="3. 모드 업데이트", value="모드 업데이트를 확인하고 업데이트 합니다", inline=False)
                    await message.channel.send(embed=embed1)
                    agreement = await client.wait_for('message', check=is_correct, timeout=30.0)
                    if agreement.content == "1":
                        await message.channel.send(
                            "만약 모드를 적용하고 싶으시다면, https://mods.factorio.com/ 에서 모드를 찾아서 링크를 첨부해주세요!")
                        await message.channel.send(f"등록할 링크를 제공해주세요!")
                        agreement = await client.wait_for('message', check=is_correct, timeout=30.0)
                        if agreement.content.find("factorio") != -1:
                            mod_name = agreement.content.split("mod/")[1]
                            await message.channel.send(mod_name)
                            url = f'https://mods.factorio.com/api/mods/{mod_name}'
                            response = requests.get(url)
                            response_json = json.loads(response.text)
                            resulta = response_json['releases'][len(response_json["releases"]) - 1]["download_url"]
                            print(resulta)
                            await message.channel.send(f" https://mods.factorio.com{resulta}")
                            url_download = f"https://mods.factorio.com{resulta}?username=0won2&token={token}"
                            r = requests.get(url_download)
                            with open(response_json['releases'][len(response_json["releases"]) - 1]["file_name"],'wb') as outfile:
                                outfile.write(r.content)
                            await message.channel.send("성공적으로 다운로드 되었습니다")
                            await message.channel.send("추가 필수 설치 모드가 있는지 찾아보겠습니다.")
                            mod_zip = zipfile.ZipFile(f"{response_json['releases'][len(response_json['releases']) - 1]['file_name']}")
                            try:
                                mod_zip.extract(f"{response_json['name']}/info.json",os.getcwd())
                                with open(f"{os.getcwd()}/{response_json['name']}/info.json") as f:
                                    essential_json = json.load(f)
                            except KeyError:
                                mod_zip.extract(f"{response_json['name']}_{response_json['releases'][len(response_json['releases']) - 1]['version']}/info.json", os.getcwd())
                                with open(f"{os.getcwd()}/{response_json['name']}_{response_json['releases'][len(response_json['releases']) - 1]['version']}/info.json") as f:
                                    essential_json = json.load(f)
                            mod_zip.close()

                            print(essential_json)
                            essential_list = list()
                            count = 0
                            embed_mod = nextcord.Embed(title="추가 모드들", color=0xff99cc)
                            while count != 1000:
                                    essential_list.append(essential_json["dependencies"][count].replace("~ ","").split(" ")[0])
                                    if essential_json["dependencies"][count].replace("~ ","").split(" ")[0] != "?" and essential_json["dependencies"][count].replace("~ ","").split(" ")[0] != "base":
                                        embed_mod.add_field(name="⠀", value=f"{count+1}.{essential_list[count]}", inline=False)
                                    if essential_json["dependencies"][count].startswith("?"):
                                        del essential_list[count]
                                        del essential_list[0]
                                        count = 999
                                    count +=1

                            if len(essential_list) == 0:
                                await message.channel.send("추가 모드가 필요하지 않습니다")
                            else:
                                await message.channel.send(embed=embed_mod)
                                await message.channel.send("추가 모드를 설치합니다. 시간이 소요될수 있습니다")
                                for a in range(len(essential_list)):
                                    mod_name = essential_list[a]
                                    await message.channel.send(mod_name)
                                    url = f'https://mods.factorio.com/api/mods/{mod_name}'
                                    response = requests.get(url)
                                    response_json = json.loads(response.text)
                                    resulta = response_json['releases'][len(response_json["releases"]) - 1][
                                        "download_url"]
                                    print(resulta)
                                    await message.channel.send(f" https://mods.factorio.com{resulta} 를 설치합니다")
                                    url_download = f"https://mods.factorio.com{resulta}?username=0won2&token=abca759aee1cd2a48aea82c3e2fa5b"
                                    r = requests.get(url_download)
                                    with open(
                                            response_json['releases'][len(response_json["releases"]) - 1]["file_name"], 'wb') as outfile:
                                        outfile.write(r.content)





                        else:
                            await message.channel.send("등록을 취소합니다!")
                    if agreement.content == "2":
                        await message.channel.send("세팅중")
                    if agreement.content == "3":
                        await message.channel.send("아직 준비중이에요!")
                else:
                    embed2 = nextcord.Embed(title="거절", description="권한이 없으셔서 모드 접근이 막혀있습니다", color=0xff0000)
                    embed2.add_field(name="1. 권한요청", value="모드 수정 권한을 요청합니다", inline=False)
                    embed2.add_field(name="2. 종료", value="모드 제어판을 종료합니다", inline=False)
                    await message.channel.send(embed=embed2)
                    agreement2 = await client.wait_for('message', check=is_correct, timeout=30.0)
                    if agreement2.content == "1":
                        await message.channel.send(f"관리자들에게 전달되었습니다. 심사후 권한 부여 여부를 알려드립니다.")
                    if agreement2.content == "2":
                        await message.channel.send("도움을 드리지 못해 죄송합니다.")
        elif agreement1.content == "2":
                await  message.channel.send("ASAP it will be abled")
        elif agreement1.content == "3":
                await  message.channel.send("취소되었습니다!")
        elif agreement1.content == "4":
                await message.channel.send("관리자들에게 전달되었습니다. 심사후 권한 부여 여부를 알려드립니다.")
