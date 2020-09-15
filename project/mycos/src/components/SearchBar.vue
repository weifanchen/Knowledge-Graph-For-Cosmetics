<template>
    <div style="width:100%;display:flex;">
        <div style="width:18%;background-color:#3A4161;margin-right:20px;padding: 50px 30px;color: #fff">
            <strong>CosChem</strong>
        </div>

        <div id="tabs" class="container">
    
            <div class="tabs">
                <a v-on:click="activetab=1" v-bind:class="[ activetab === 1 ? 'active' : '' ]">Product</a>
                <a v-on:click="activetab=2;clickAdvanced=false" v-bind:class="[ activetab === 2 ? 'active' : '' ]">Advanced</a>
                <a v-on:click="activetab=3" v-bind:class="[ activetab === 3 ? 'active' : '' ]">Collections</a>
            </div>

            <div class="content">
                <div v-if="activetab === 1" class="tabcontent">
                    <div class='basic-search'>
                        <AutoComplete
                            v-model="value"
                            :data="suggestions"
                            :filter-method="filterMethod"
                            placeholder="input here"
                            style="width:40%; max-height: 100px;">
                        </AutoComplete>
                        <div class='input-field'>
                            <!-- <input id='search' type='text' placeholder='What are you looking for?'> -->
                            <div class="icon-wrap">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" @click="getProduct">
                                    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path>
                                </svg>
                            </div>
                        </div>
                        <!-- {{value}} -->
                        <!-- <div class="icon-wrap">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" @click="getProduct">
                                <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path>
                            </svg>
                        </div> -->
                    </div>


                    <div v-if="productLoaded" style="padding: 50px 0 0 24px; display:flex;">
                        <div class='leftPanel' style="width:50%">
                            <div style='display:flex;padding-bottom:20px;'>
                                <img src="https://static-reg.lximg.com/images/product_images/closeup_16679_FRESH_WEB_9686032ffd7987e8056a4105ab3db4f4282a2c9e_1523777995.png" style="max-height:160px;width:140px;border-radius: 20px; border:1.5px solid #F6F4F9">

                                <div style="padding-left: 50px; width:80%;padding-right: 200px;">
                                    <p>Origin</p>
                                    <p style="font-size:22px; font-weight:bold;color:#505050">Soy Face Cleanser</p> 
                                    <button id='add' type="button" @click='putBag'>Add to Collection</button>
                                    <!-- <p><span>Category</span><span style='display:inline-block; padding-left:10px;'>Moisturizer</span></p>
                                    <p><span>Category</span><span style='display:inline-block; padding-left:10px;'>Moisturizer</span></p>
                                    <p><span>Category</span><span style='display:inline-block; padding-left:10px;'>Moisturizer</span></p>
                                    <p><span>Category</span><span style='display:inline-block; padding-left:10px;'>Moisturizer</span></p> -->
                                    <p style="margin-top:20px;"></p>
                                    <div style="width:100%; height:45px">
                                        <p style="float: left"><strong>Category</strong><br>on the left</p>
                                        <p style="float: right"><strong>Category</strong><br>on the right</p>
                                    </div>
                                    <div style="width:100%; height:45px; margin-top:10px">
                                        <p style="float: left"><strong>Category</strong><br>on the left</p>
                                        <p style="float: right"><strong>Category</strong><br>on the right</p>
                                    </div>
                                    <!-- <p></p>
                                    <span><strong>Category</strong> <br>Moisturizer</span>
                                    <span><strong>Category</strong> <br>Moisturizer</span> -->
                                    <!-- <span>Category Moisturizer</span>
                                    <span>Category Moisturizer</span>
                                    <span>Category Moisturizer</span>                                 -->
                                </div>

                            </div>
                            <div>
                                <p style="font-size:20px;;color:#505050; margin-bottom:15px;margin-top:30px">Similar products</p> 
                                <div style='margin-left:5px;display:flex;margin-right:30px'> 
                                    <div class='similar' style='height:80px;padding:10px 15px;' v-for="item in similar[2025633]" v-bind:key="item.id">
                                        <p><strong>{{item.name}}</strong></p>
                                        <p>{{item.product_name}}</p>
                                        <p>{{item.star}}</p>
                                    </div>
                                </div>
                            </div>


                        </div>
                        <!-- <div style="width:6%; border-left:1px solid #C1C1C1;margin-top:2%;background-color:#EDF3F8"></div> -->
                        <div style="width:45%;margin-top:4%;padding-left:8%;border-left:1px solid #C1C1C1">
                            <!-- <span style="font-size:20px; font-weight:bold;"></span> -->
                                <strong>What is in it ...</strong>
                                <br><br>
                                <!-- <ul style="list-style-type:none;border:1.5px solid #F6F4F9"> -->
                                <ul style="list-style-type:none;box-shadow: 0 3px 6px rgba(0,0,0,0.01), 0 3px 6px rgba(0,0,0,0.01);">
                                    <li class='ingredient' style='height:50px;padding:15px 15px;border-bottom:0.5px solid #F6F4F9;font-size: 15px;' v-for="item in items" v-bind:key="item.id">
                                        <strong>{{item.name}}</strong>
                                        <span style='float:right;'>Acne: 5 | Acne: 5 | Acne: 5</span> 
                                    </li>
                                </ul>
                                <!-- <List border size="small">
                                    <ListItem v-for="item in items" v-bind:key="item.id">{{item.name}}</ListItem>
                                </List>  -->
                        </div>


                    </div>

                </div>
                <div v-if="activetab === 2" class="tabcontent">
                    <div class='advanced-search' v-if="!clickAdvanced">
                        <div style='display:flex;'>
                            <div style='float:left;width:47%'>
                            <p><strong>CATEGORY</strong></p>
                                <Select v-model="selectCat" multiple placeholder='Choose Category'>
                                    <OptionGroup label="Moisturizers">
                                        <Option v-for="item in categoryList.Moisturizers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Treatments">
                                        <Option v-for="item in categoryList.Treatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>      
                                    <OptionGroup label="Cleansers">
                                        <Option v-for="item in categoryList.Cleansers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Masks">
                                        <Option v-for="item in categoryList.Masks" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup> 
                                    <OptionGroup label="Eye Care">
                                        <Option v-for="item in categoryList.EyeCare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Sun Care">
                                        <Option v-for="item in categoryList.SunCare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup> 
                                    <OptionGroup label="Lip Treatments">
                                        <Option v-for="item in categoryList.LipTreatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Self Tanners">
                                        <Option v-for="item in categoryList.SelfTanners" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>  
                                    <OptionGroup label="Skincare">
                                        <Option v-for="item in categoryList.Skincare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Wellness">
                                        <Option v-for="item in categoryList.Wellness" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>      
                                    <OptionGroup label="Body Moisturizers">
                                        <Option v-for="item in categoryList.BodyMoisturizers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="High Tech Tools">
                                        <Option v-for="item in categoryList.HighTechTools" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup> 
                                    <OptionGroup label="Hair Styling Treatments">
                                        <Option v-for="item in categoryList.HairStylingTreatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Bath Shower">
                                        <Option v-for="item in categoryList.BathShower" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup> 
                                    <OptionGroup label="Others">
                                        <Option v-for="item in categoryList.Others" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>    
                                </Select>
                            </div>
                            <div style='margin-left:25px;float:right;width:47%'>
                                <div class='filter'>
                                    <p><strong>ACNE</strong></p>
                                    <label><input v-model="acne" type="radio" name="acne" v-bind:value="1"/><span data-points="1">1</span></label>
                                    <label><input v-model="acne" type="radio" name="acne" v-bind:value="2"/><span data-points="2">2</span></label>
                                    <label><input v-model="acne" type="radio" name="acne" v-bind:value="3"/><span data-points="3">3</span></label>
                                    <label><input v-model="acne" type="radio" name="acne" v-bind:value="4"/><span data-points="4">4</span></label>
                                    <label><input v-model="acne" type="radio" name="acne" v-bind:value="5"/><span data-points="5">5</span></label>
                                </div>
                            </div>
                        </div>
                        <!-- <span>ADVANCED SEARCH</span> -->
                        <div class='filter' style='width:60%; display: flex;margin-bottom:15px;'>
                            <span style='displat:inline-block; padding: 5px 50px 0 2px;font-size:14px; font-weight:bold;'>Category</span>
                            <Select v-model="selectCat" multiple placeholder='Choose Category'>
                                <OptionGroup label="Moisturizers">
                                    <Option v-for="item in categoryList.Moisturizers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>
                                <OptionGroup label="Treatments">
                                    <Option v-for="item in categoryList.Treatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>      
                                <OptionGroup label="Cleansers">
                                    <Option v-for="item in categoryList.Cleansers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>
                                <OptionGroup label="Masks">
                                    <Option v-for="item in categoryList.Masks" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup> 
                                <OptionGroup label="Eye Care">
                                    <Option v-for="item in categoryList.EyeCare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>
                                <OptionGroup label="Sun Care">
                                    <Option v-for="item in categoryList.SunCare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup> 
                                <OptionGroup label="Lip Treatments">
                                    <Option v-for="item in categoryList.LipTreatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>
                                <OptionGroup label="Self Tanners">
                                    <Option v-for="item in categoryList.SelfTanners" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>  
                                <OptionGroup label="Skincare">
                                    <Option v-for="item in categoryList.Skincare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>
                                <OptionGroup label="Wellness">
                                    <Option v-for="item in categoryList.Wellness" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>      
                                <OptionGroup label="Body Moisturizers">
                                    <Option v-for="item in categoryList.BodyMoisturizers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>
                                <OptionGroup label="High Tech Tools">
                                    <Option v-for="item in categoryList.HighTechTools" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup> 
                                <OptionGroup label="Hair Styling Treatments">
                                    <Option v-for="item in categoryList.HairStylingTreatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>
                                <OptionGroup label="Bath Shower">
                                    <Option v-for="item in categoryList.BathShower" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup> 
                                <OptionGroup label="Others">
                                    <Option v-for="item in categoryList.Others" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </OptionGroup>    
                            </Select>
                        </div>
                        <div class='filter' style='width:40%; display: flex;padding-bottom:15px;font-size:14px; font-weight:bold;'>
                            <span style='displat:inline-block; padding: 5px 77px 0 2px;'>Acne</span>
                            <!-- <Slider v-model="acne" max=5 show-input></Slider> -->
                            <label><input v-model="acne" type="radio" name="acne" v-bind:value="1"/><span data-points="1">1</span></label>
                            <label><input v-model="acne" type="radio" name="acne" v-bind:value="2"/><span data-points="2">2</span></label>
                            <label><input v-model="acne" type="radio" name="acne" v-bind:value="3"/><span data-points="3">3</span></label>
                            <label><input v-model="acne" type="radio" name="acne" v-bind:value="4"/><span data-points="4">4</span></label>
                            <label><input v-model="acne" type="radio" name="acne" v-bind:value="5"/><span data-points="5">5</span></label>
                            <!-- <span>value: {{acne}}</span> -->

                        </div>
                        <div class='filter' style='width:40%; display: flex;padding-bottom:15px;font-size:14px; font-weight:bold;'>
                            <span style='displat:inline-block; padding: 5px 66px 0 2px;'>Irritant</span>
                            <!-- <Slider v-model="acne" max=5 show-input></Slider> -->
                            <label><input v-model="irri" type="radio" name="irri" v-bind:value="1"/><span data-points="1">1</span></label>
                            <label><input v-model="irri" type="radio" name="irri" v-bind:value="2"/><span data-points="2">2</span></label>
                            <label><input v-model="irri" type="radio" name="irri" v-bind:value="3"/><span data-points="3">3</span></label>
                            <label><input v-model="irri" type="radio" name="irri" v-bind:value="4"/><span data-points="4">4</span></label>
                            <label><input v-model="irri" type="radio" name="irri" v-bind:value="5"/><span data-points="5">5</span></label>
                            <!-- <span>value: {{irri}}</span> -->
                        </div>
                        <div style='width:70%; display: flex;padding-bottom:15px;font-size:14px; font-weight:bold;'>
                            <span style='displat:inline-block; padding: 5px 79px 0 2px;'>FDA</span>
                            <CheckboxGroup v-model="fda">
                                <Checkbox label="Fragrance" border></Checkbox>
                                <Checkbox label="Preservative" border></Checkbox>
                                <Checkbox label="Alchocal" border></Checkbox>
                            </CheckboxGroup>
                        </div>
                        <Button shape="circle" icon="ios-search" @click="getMsg"></Button>

                    </div>
                    <div v-if="clickAdvanced && !msgLoaded">
                        Loading
                    </div>
                    <div v-if="clickAdvanced && msgLoaded" style="padding: 50px">
                        <!-- Hello!!!
                        {{msg}} -->
                        <List item-layout="vertical">
                            <ListItem v-for="item in msg" :key="item.title">
                                <ListItemMeta :title="item.title" :description="item.description" />
                                Origin | Moisturizers
                                {{ item.content }}
                                <template slot="action">
                                    <li>
                                        <Icon type="ios-star-outline" /> 123
                                    </li>
                                    <li>
                                        <Icon type="ios-thumbs-up-outline" /> 234
                                    </li>
                                    <li>
                                        <Icon type="ios-chatbubbles-outline" @click='getProduct'/> 345
                                    </li>
                                </template>
                                <template slot="extra">
                                    <img src="https://dev-file.iviewui.com/5wxHCQMUyrauMCGSVEYVxHR5JmvS7DpH/large" style="width: 280px">
                                </template>
                            </ListItem>
                        </List>
                    </div>
                </div>
                <div v-if="activetab === 3" class="tabcontent">
                    Open your eyes, look up to the skies and see
                </div>
            </div>

        </div>
    </div>

</template>

<script>
import categoryList from '@/assets/categoryList.js'
// import product from '@/assets/product3.js'
import product from '@/assets/product.json'
import axios from 'axios';
import json from '@/assets/similar_product.json'




export default{
    mounted(){
        this.suggestions = product;
        this.dataLoaded = true;
        // console.log(this.suggestions)
    },
    created(){
        this.categoryList = categoryList;
    },
    data(){
        return{
            value: '',
            suggestions:[],
            dataLoaded: false,
            categoryList: [],
            selectCat: [],
            activetab: 1,
            acne: 1,
            irri: 1,
            fda: [],
            clickAdvanced: false,
            msgLoaded: false,
            clickBasic: false,
            productLoaded: false,
            msg: '',
            // similar: [
            //     {'id':1, 'name': "Hello"},
            //     {'id':2, 'name': "is"},
            //     {'id':3, 'name': "me"},
            // ],
            similar: json,
            items: [
                {'id':1, 'name': "Hello"},
                {'id':2, 'name': "is"},
                {'id':3, 'name': "me"},
                {'id':4, 'name': "Hello"},
                {'id':5, 'name': "is"},
                {'id':6, 'name': "me"},
                {'id':7, 'name': "Hello"},
                {'id':8, 'name': "is"},
                {'id':9, 'name': "me"},
                {'id':10, 'name': "Hello"},
                {'id':11, 'name': "is"},
                {'id':12, 'name': "me"},
                {'id':13, 'name': "Hello"},
                {'id':14, 'name': "is"},
                {'id':15, 'name': "me"},
                {'id':16, 'name': "Hello"},
                {'id':17, 'name': "is"},
                {'id':18, 'name': "me"},
                {'id':19, 'name': "Hello"},
                {'id':20, 'name': "is"},
                {'id':21, 'name': "me"},
            ],
            mycollect: [],
        }
    },
    methods:{
        getProduct(){
            // console.log(this.similar['1172246'])
            this.productLoaded = false;
            this.clickBasic = true;
            this.productLoaded = true;
            // const path = 'http://localhost:5000/';
            // axios.get(path,  {
            //     params: {
            //         //product_id: this.selected.product_id 
            //         type: 'Basic',
            //         product: this.value,
            //     }
            //     }).then((res) => {
            //         console.log(res);
            //         this.msg = res.data;
            //         // this.$router.push({
            //         // name: 'result',
            //         // params: {
            //         //     response: res.data
            //         // }
            //     // });
            //     })
            //     .catch((error) => {
            //         // eslint-disable-next-line
            //         console.error(error);
            //     });
            this.activetab = 1;
            // this.value = 'from Advanced'

        },
        getMsg(){
        this.msgLoaded = false;
        this.clickAdvanced = true;
        const path = 'http://localhost:5000/';
        axios.get(path,  {
            params: {
                //product_id: this.selected.product_id 
                type: 'Advanced',
                categories: this.selectCat,
                acne: this.acne,
                irri: this.irri,
                fda: this.fda,
            }
            }).then((res) => {
                console.log(res);
                this.msg = res.data;
                // this.$router.push({
                // name: 'result',
                // params: {
                //     response: res.data
                // }
            // });
            })
            .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
            });
            // this.msg = [
            //         {
            //             title: 'This is title 1',
            //             description: 'This is description, this is description, this is description.',
            //             avatar: 'https://dev-file.iviewui.com/userinfoPDvn9gKWYihR24SpgC319vXY8qniCqj4/avatar',
            //             content: 'This is the content, this is the content, this is the content, this is the content.'
            //         },
            //         {
            //             title: 'This is title 2',
            //             description: 'This is description, this is description, this is description.',
            //             avatar: 'https://dev-file.iviewui.com/userinfoPDvn9gKWYihR24SpgC319vXY8qniCqj4/avatar',
            //             content: 'This is the content, this is the content, this is the content, this is the content.'
            //         },
            //         {
            //             title: 'This is title 3',
            //             description: 'This is description, this is description, this is description.',
            //             avatar: 'https://dev-file.iviewui.com/userinfoPDvn9gKWYihR24SpgC319vXY8qniCqj4/avatar',
            //             content: 'This is the content, this is the content, this is the content, this is the content.'
            //         }                
            // ]
            
            this.msgLoaded = true;
            console.log('click image');
        },

        filterMethod (value, option) {
            return option.toUpperCase().indexOf(value.toUpperCase()) !== -1;
        },

        putBag(){
            this.mycollect.push("Kiwi")
            console.log(this.mycollect)
        }
        
    }
}
</script>

<style>

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* STYLING */
.container {  
    max-width: 620px; 
    min-width: 100%;
    /* margin: 40px auto; */
    font-family: "Nunito Sans", Arial, Helvetica, sans-serif;
    color: #888;
}

/* Style the tabs */
.tabs {
    overflow: hidden;
    margin-left: 20px;
    margin-bottom: -2px; 
}

.tabs ul {
    list-style-type: none;
    margin-left: 20px;
}

.tabs a{
    float: left;
    cursor: pointer;
    padding: 12px 24px;
    transition: background-color 0.2s;
    /* border-bottom: 1.5px solid #ccc; */
    border-right: none;
    /* background-color: #f1f1f1; */
    border-radius: 10px 10px 0 0;
    font-weight: bold;
    color: #888888;
}

.tabs a:last-child { 
    /* border-right: 1px solid #ccc; */
}

/* Change background color of tabs on hover */
.tabs a:hover {
    border-bottom: 1.5px solid #CBCBCB;
    /* background-color: #aaa; */
    color: #2C3542;
}

/* Styling for active tab */
.tabs a.active {
    border-bottom: 1.5px solid #7889B3;
    background-color: #fff;
    color: #484848;
    /* border-bottom: 2px solid #fff; */
    cursor: default;
}

/* Style the tab content */
.tabcontent {
    min-height: 730px;
    padding: 20px 20px;
    border-right: 1.2px solid #ccc;
    border-left: 1.2px solid #ccc;
    border-bottom: 1.2px solid #ccc;
    border-radius: 10px;
    box-shadow: 3px 3px 6px #e1e1e1
}

form {
    width: 100%;
    max-width: 790px;
    margin: 0;
}

/* .searchPanel {
    width: 100%;
} */

.basic-search {
    padding: 10px 0 0 20px;
    /* box-shadow: 0px 8px 20px 0px rgba(0, 0, 0, 0.15); */
    /* overflow: hidden;
    border-radius: 20px;
    margin-bottom: 5px;
    border: 1.5px solid #FFE659;
    height: 40px;
    width: 40%; */
}

.input-field {
    width: 100%;
    position: relative;
    padding: 0 20px;
}

input {
    height: 100%;
    border: 0;
    display: block;
    width: 100%;
    padding: 10px 80px 10px 40px;
    font-size: 18px;
    height: 36px;
    color: #333333;
    background: transparent;
    border: none;
    outline: none;
    /* background: linear-gradient(to right, #2c6dd5 0%, #2c6dd5 28%, #ff4b5a 91%, #ff4b5a 100%); */
    /* font-family: 'Lato', sans-serif; */
}

::placeholder{
    color: #333333 0.3;
}

.icon-wrap {
    position: absolute;
    top: -15px;
    left: 41%;
    /* right: 0; */
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    width: 40px;
    height: 100%;
}

path {
    fill: #7889B3;
}

.ivu-select-dropdown {
    width: inherit;
    max-height: 200px;
    overflow: auto;
    margin: 5px 0;
    padding: 10px 10px !important;
    background-color: #fff;
    box-sizing: border-box;
    border-radius: 4px;
    box-shadow: 0 1px 6px rgba(0,0,0,.2);
    position: absolute;
    z-index: 900;
}

.advanced-search{
    padding: 10px 700px 0 20px;
    /* box-shadow: 0px 8px 20px 0px rgba(0, 0, 0, 0.15);
    border-radius: 10px; */
}

.advance-search span {
    font-size: 14px;
    font-weight: bold;
    color: #555;
    display: block;
    margin-bottom: 26px;
}

.filter label {
    display: block; 
    /* padding: 5px;  */
    position: relative; 
    padding-left: 30px;
    padding-right: 20px;
}


.filter label input {display: none;}

.filter label span {
    /* border: 1px solid #ccc; */
    background: #f1f1f1;
    width: 28px;
    height: 28px;
    position: absolute;
    overflow: hidden;
    /* line-height: 1; */
    text-align: center;
    border-radius: 100%;
    font-size: 14pt;
    left: 0;
    top: 50%;
    margin-top: -10px;
}

.filter label span:hover{
   background: #333333; 
}

/* input:checked + span {
    background: #ccf; 
    border-color: #ccf;} */


.filter input:checked + span[data-points="1"] {
    background: #7f7d33; 
    opacity: 0.6;
    }
.filter input:checked + span[data-points="2"] {
    background: #f1f1cf; 
    }
.filter input:checked + span[data-points="3"] {
    background: #edc894; 
    }
.filter input:checked + span[data-points="4"] {
    background: #ea967c; 
    }
.filter input:checked + span[data-points="5"] {
    background: #a6181a; 
    opacity: 0.6;
    }

.ivu-checkbox {
    display: none !important;
}

.ivu-checkbox+span, .ivu-checkbox-wrapper+span{
    margin-right: 0px !important; 
}

.ivu-checkbox-wrapper-checked.ivu-checkbox-border {
    border-color: #f1f1f1 !important;
}

.ivu-input {
    display: inline-block;
    width: 100%;
    height: 32px;
    line-height: 1.5;
    padding: 4px 17px !important;
    font-size: 14px;
    border: 1px solid #dcdee2;
    border-radius: 12px !important;
    color: #515a6e;
    background-color: #fff;
    background-image: none;
    position: relative;
    cursor: text;
    transition: border .2s ease-in-out,background .2s ease-in-out,box-shadow .2s ease-in-out;
}

.ivu-input:focus {
    border-color: #f1f1f1 !important;
    outline: 0;
    box-shadow: none !important;
}

.ivu-input:hover {
    border-color: #f1f1f1 !important;
}

.ivu-checkbox-border {
    border: 1px solid #dcdee2;
    border-radius: 4px;
    height: 28px !important;
    line-height: 28px !important;
    padding: 0 8px !important;
    transition: border .2s ease-in-out;
}

.similar {
    background-color: #F6F4F9;
    border-radius: 20px;
    width: 180px;
    margin-right: 30px;
}
  
#add {
    background-color: rgb(246, 244, 249);
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
    color: rgb(120, 137, 179);
    margin-top: 6px;
    font-weight: bolder;
}

#add:active {  
    outline: none; 
    background-color: #333333;  
}

#add:focus {  
    outline: none; 
}

.ivu-list-container{
    border: #fff !important;
}

.ivu-auto-complete.ivu-select-dropdown {
    max-height: 300px !important;
}

/* input:checked ~ label[for="slide1"],
input:checked ~ label[for="slide2"],
input:checked ~ label[for="slide3"],
input:checked ~ label[for="slide4"] {
  background: #333;
} */




</style>